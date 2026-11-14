# task25: which of Saukko Labs' H1 2027 pretraining runs will not finish inside the GPU windows reserved for them, and how much longer than the benchmark each run will take

## Draw

Subdomain: General Statistics & Data Science (Benchmarking and ablations)
Analysis type: Comparative Analysis & Explanation
Answer shape: bridge: for each H1 2027 run, the throughput benchmark's days bridged cause by cause to the expected
  days with an 80 per cent range, against the run's reserved window, with the late set and each late run's fix on
  top; the 2026 bridge from benchmark days to actual days is the record each cause is measured on
Weight: modeling: every cause has to be built at a condition no 2026 run reached, or measured where the 2027 plan
  will not show it (the slowest of up to a thousand data-parallel ranks on a long-document mix, best-fit packing on
  a long-form mix, hall B held to its contracted power by a research pool that backs off as the reservations near
  it, a block laid across hall B's two pods, which the benchmark's one-pod slice cannot show); the last three builds
  sat in modeling (task24), measurement (task20) and a hard-to-measure quantity (task7), so the weight repeats
  task24's (guard WARN): the answer shape (a bridge, not a forecast with drivers), the decision form and every
  lesson but one differ
Data-native sentence: every 2026 throughput figure is recorded at the grain of the system that produced it (a
  50-step interval of one run, one rank's share of a profiled step, the documents of one packed sequence, a
  five-minute reading of a hall's draw and node states, the node list of one run's segment, one work order), and each
  H1 2027 run sits at a data-parallel width, document mix, packing rule, hall load or block placement no 2026 run
  reached, so its days can only be built at the grain where each cause is decided
People: Pia Kuosmanen (head of training infrastructure, whose workbook and note the golden are), Esa Airaksinen
  (chairs the compute committee that holds the H1 2027 reservations), Marja Laine (data team lead, owns the 2027
  mixes); drawn with `guard.py names --geo FI --seed 2511`. None appears in the prompt.

The world. Saukko Labs Oy, a fictional Espoo AI lab, trains its own Kide family of dense language models on two
leased GPU halls at Pohjoisvirta Datacenters' Kaivola campus: hall A (H100) and hall B (H200, larger, in two pods
the node names carry, leased on a contracted IT load below its full-load draw). The infrastructure team benchmarks
every model configuration on a 64-node slice with a synthetic packed corpus before the compute committee reserves
blocks and windows for the half year; the 2027 reservations were sized on those benchmarks. Nodes no reservation
holds run a research pool whose scheduler stops admitting jobs as the load without it nears the contract. The 2026
record holds about sixty runs' step logs, profiled per-rank step timings and packing logs for a sample of runs,
interruptions, node allocations, the provider's five-minute hall draw and work orders, and the 2027 roadmap (with
each run's block of rows), configs, data mixes and works calendar.

## Stump screen

Written at the draw on 2026-11-13 and rewritten at the repair of 2026-11-14, after the reviewer's audit run on this
architecture (`runs/holistic_audit_2026-11-13.md`). That run reproduced all eleven benchmark days and the 2026
GPU-days held, modelled the rank imbalance, replayed best-fit packing, rebuilt the censored power meter, priced
interruptions and the works overrun, reached the same seven late runs and caught a capacity conflict in hall B: each
move is a reflex from then on (R84 to R90 in `precedents.json`), so the draw's first three stumps (the slowest rank,
best-fit padding, hall B's throttle) are priced Right and stand only as results. Two new candidates went through the
eleven tests of `references/stump-screen.md` and the numbers were prototyped on scratch arrays (`scratchpad/p8/`)
before the generator changed. No one sentence rescues both: the first is about where a block sits, the second about
what the pool does as the reservations grow.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A job whose nodes sit in both of hall B's pods sends every gradient reduction over the spine between them and runs about a fifth slower at every step; the benchmark's 64-node slice sits in one pod on an idle hall, so no benchmark figure carries it; the 2027 ledger lays exactly one block (kide-8b-v4, rows 16 and 17) across the boundary because the pods cannot be tiled by the plan's block sizes | the benchmark's rate and the cost model's step carried to every block, the pod named in each node list left unread and the residual filed as start-ups and drift (N09 the topology assumed uniform over the history, N04 a transfer past the benchmark's range) | the 2026 node allocations (the node names carry the pod) against each run's steady step over the step its benchmark, mix and width predict; the roadmap's block column | none (not a reflex: no reflex id carries a topology term and the audit run's moves stop at the cost model; nothing filed names a pod; two records at two grains; a plausible shallower story, the residual under "other"; across the data: three registered runs and the scale test in 2026, the ledger's one block; worth one member of the call) | kept (P) |
| Hall B's research pool takes its 2026 mean share (a third) of the nodes no reservation holds, whatever the reservations hold; its scheduler in fact stops admitting jobs as the load without it nears the contract and has none running by 97 per cent of it, so with 800 nodes reserved (February to mid-March) the pool is off and the hall is nearly unthrottled, while a pool at its mean share adds about eighty nodes of load | a mean share used where a response is needed (L15 a behavioural response assumed instead of measured, N28 an input another process re-sets held at its latest supplied value) | node states less the registry's held nodes, against the load the registered runs alone put on the hall through the fitted draw line, in the 2026 intervals at 512 reserved and at 768 or more | none (not a reflex: the audit run's replay held the pool at one share; two records at two grains; the shallower story is a throttle that is simply larger; across the data: 2026's 27 days at 768 or more reserved and eight months at lighter loads; worth one member) | kept (Q) |
| Provider works ran well past their planned hours in 2025 and 2026 and the 2027 calendar books a hall A re-cabling and a hall B chilled-water upgrade inside reserved windows | works at their planned hours (N22, N03, L46) | the provider's 2025-26 work orders, planned against actual hours by type | 2 (the audit run priced the overrun unprompted, R88) | kept as a supporting result: each window's days lost to works are a column of the 2027 bridge, priced Right by the careful pass |
| The slowest data-parallel rank sets each step, best-fit packing pads a long-form mix, and the provider holds hall B to its contract on a meter that reads the cap | the mean rank, full sequences, a meter taken as the draw (N04, L22, L26, L38) | per-rank timings with packing manifests, the packing replay, the meter against node states | 2 (the audit run made each, R84 to R86) | dropped as stumps of this draw; kept as results R3, R4 and R5 |
| Each model draws its own power per node (a published utilisation by size) so hall B's would-be draw depends on the mix of runs | a draw per node taken as one constant | the meter against the allocation record by model mix | 1 and 4 (a closed composition card; the mix changes only the intercept the line already fits) | dropped |
| A neighbouring pod's load slows a job through shared spine capacity | the idle benchmark slice taken as the production fabric | the step logs of jobs beside a large run | 1 (the client's closed spillover card) | dropped |
| A trainer release (kd-train 2.4) changed the step by about three per cent from 1 August | a step time taken as one process throughout 2026 | the trainer version column against steady steps | 8 and the hidden-factor screen (a break built into the data that one cross-tab shows; one sentence leaves a dummy) | dropped |
| One rack in hall B runs slow under load | a passed burn-in taken to certify a node | per-rank timings by node | 8 (a defect only in the units that decide the answer) | dropped |

## Deep reasoning

Task type: Benchmarking and ablations (controlled evaluation, isolating component effects): the infrastructure
  team's throughput benchmark is the controlled evaluation, and the work is isolating each component of the gap
  between it and production runs, measuring each on the record where it is decided and carrying it to runs at
  conditions the benchmark and the record never reached
Domain test: each result is the analysis type's own statistical object: an expected maximum over data-parallel
  ranks of a compound per-rank load (order statistics of a sum whose terms are quadratic in document length), the
  expected fill of an online best-fit packing process under a heavy-tailed length mix, a threshold response estimated
  on the intervals a hall crossed its contracted power (with the meter reading the cap, so the excess is rebuilt from
  the allocation record), the step's penalty for a job laid across two pods read from the runs that were, and a
  research pool's share of the free nodes as a function of the load the reservations put on the hall, interruption
  rates and their cost, an overrun distribution from comparable works, and a bridge whose items add to the gap
Swap: "the long-context runs need 15 per cent more days because each step waits for the rank whose sequences hold
  the long documents" read with warehouse nouns ("each wave waits for the picker whose orders hold the bulky items")
  keeps a max over parallel workers but loses the packing process that sets each worker's load, the benchmark it is
  bridged from, the cap read off a metered hall, the spine between two pods a job's nodes are laid across and the
  token budget a padded sequence does not count; the chain stops making sense outside a synchronous data-parallel
  trainer in a power-capped, two-pod hall
Where the weight sits: modeling and measurement: R5 (the throttle response measured on 2026's capped intervals once
  their excess is rebuilt, replayed on hall B's 2027 load with the pool at the share the registered load leaves it),
  R10 (the pod penalty read from the allocations and the steady steps, applied to the ledger's blocks) and R11 (the
  pool's busy nodes as a function of the reserved load, measured at light and heavy loads in 2026 and read at the
  plan's) are each a model built and checked on its own record; R3 and R4 (the rank cost model and the packing replay)
  are built the same way and are made unprompted
Layer 1: the trainer's step counter restarts at zero after some resumes (a v2.3 logging fault) and the logger
  re-sends its last buffer after a restart, so step-log rows repeat; three runs were renamed at a resume (the
  registry carries both names); the provider's hall meter and work orders are in Helsinki local time while every
  Saukko log is UTC; the hall meter drops intervals during collector outages; checkpoint sizes are logged in GiB by
  the trainer and GB by the storage system; a cooling fault slowed hall A's row 6 under sustained load from 14
  September to its repair on 19 October 2026; none decides a result, each cleaned the same way by every careful run
Not one thing: the call rests on two members a run can get wrong (kide-8b-v4, late only with the pod penalty; kide-34b-v3, fitting
  only with the pool's back-off), each opened by its own stump, beside nine members every route files as the golden
  does; a run that has found one still files the other wrongly, and each stump has its own graded result (R10, R11
  and R5) and its own cells in the bridge, so the one-fact sentence rescues 2 of the 12 results
One-fact test: the most useful single sentence is "a job whose nodes sit in both of hall B's pods runs about a fifth slower than the benchmark's idle slice"; it rescues R10 and the pod cell of
  the bridges and leaves the pool's response, kide-34b-v3's verdict and the hall B runs' days to their own work (effort.py:
  the largest hint rescues 2 of 12 results)
Not semantics: every field, unit and clause read correctly (the token budget counts real tokens, a window runs from
  00:00 UTC on its first day, the meter is the hall's IT load, a block's rows are the nodes it holds) still leaves
  the reflex route at two verdicts wrong: the hurried figures come from carrying a rate and a mean share to
  conditions that change them, not from a reading
Not rule application: no filed procedure computes a run's days; the reservation terms file what a window is, what
  counts as finishing, that freed nodes run backfill and that a later run waits for nodes still held, and every
  remaining step (the per-rank cost model, the maximum over ranks, the packing fill, the excess and its response,
  the pod penalty, the pool's response, the interruption cost) is estimated
Estimand: the reservation terms file each run's window (00:00 UTC on the first reserved day to 00:00 UTC on the day
  after the last), that a run finishes when the trainer has counted its token budget of training tokens (padding
  excluded), that the committee's test is whether the expected finish falls inside the window, that a block's nodes
  stay busy to the window's end (backfill after an early finish) and are held until a late run finishes, and the
  GPU-days held and the 2026 population; the roadmap files each run's block of rows; the prompt asks for expected
  days, an 80 per cent range, the finish date, and the 2026 bridge from benchmark-implied GPU-days to GPU-days held
No decoy: nothing in the pack is written to carry a wrong answer; the benchmark file is the team's real measurement
  of each configuration on its own harness (synthetic corpus, 64-node slice in one pod, an idle hall), reproduces
  exactly by its stated method, and answers a shallower quantity; the asks price it on the golden's footing (each
  run's benchmark days and its bridge to expected days)
No replay: no result re-derives a published figure; the benchmark days are the bridge's starting point, not a figure
  to reproduce, and no stated number in the pack is wrong
Pinned: rivals run on the clean truth in `generator/results.py` (`battery`): fifteen variants of the hall B chain and
  five of the cost model and the rates, each filing the same seven late runs and moving no run's days by more than
  2.3 per cent; the pinning list names every constant and its home
Run forecast: R10 lost to dismissed own evidence (the node lists name the pod and the run files the residual under
  start-ups and drift); R5 and R11 lost to a method shortcut (the pool at its 2026 mean share where the response was
  needed); R8, R12, R13 and R14 lost as an unfinished chain on the hall B runs; R9 lost on kide-8b-v4 and kide-34b-v3; R2 partly
  (the pod item left in the residual); R1, R3, R4 and the interruption and works columns are earned by reflex
Strategy label: UNTESTED (own: no client strategy bridges a throughput benchmark to production runs at conditions
  never run; the machine-learning strategies 1 to 4 are loss and evaluation curves)
Depth level: 4: two necessary stumps (P the pod boundary, Q the pool's back-off) each opening a member of the call
  (kide-8b-v4 and kide-34b-v3), each dropped alone on a distinct wrong late set, neither sufficient alone; the slowest rank, the
  padding, the throttle on the rebuilt excess, the works overrun, interruptions and the ledger are reflexes priced
  Right (R84 to R90); level 5 would need a third stump opening a third member
Lesson: a benchmark measures throughput at the conditions it ran (a short synthetic mix, 64 ranks in one pod, an idle
  hall, a sequential packer), and production days come from the conditions a run meets: a model learns to bridge a
  controlled measurement to a deployment cause by cause, each cause measured where it is recorded, and to read where
  a unit sits (a pod) and what a shared supply does as the plan loads it (the pool backing off) rather than carry one
  ratio or one mean share

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the 2026 ledger: GPU-days held by the 2026 runs (total and by hall), reconciled to the scheduler's allocation record | assembly-reconciliation | CAR-2027-1 section 6's GPU-days held and its 2026 population; replayed and renamed rows resolved | exact to 0.5 per cent | narrow look at broad data: replayed rows counted or renamed runs split (made right by reflex, R90) | independent: registry, allocation record | Ask 3 |
| R2 | the 2026 bridge from benchmark-implied GPU-days to GPU-days held, by cause (mix attention, slowest rank, padding, blocks across both pods, hall B throttle, row 6 cooling, interruptions and restarts, works, residual) | decomposition-attribution | the stated attribution order in the answer blocks; each cause measured on its own record | each item within 12 per cent of its own size or 1,500 GPU-days, the total exact | dismissed own evidence: the straddling runs' extra time left in the residual beside start-ups and drift, though the node lists name the pod | R1 | Component 4 |
| R3 | the per-rank cost model (the attention coefficient) and each 2027 long-context run's slowest-rank overhead over its mean rank | modeling | the profiled 2026 runs' per-rank timings joined to the packing log; each run's config (ranks, sequences per rank) and the 2027 length sample | overhead within 3 points | method shortcut: the mean rank or the full-context formula (made right by reflex, R84) | independent: traces, packing log, 2027 sample | Ask 4 |
| R4 | each best-fit 2027 run's packing fill (real tokens per sequence position) | modeling | the 2027 configs' packing rule and the 2027 length sample; the Q4 2026 packing logs | within 1.5 points | method shortcut: full sequences (made right by reflex, R85) | independent: 2027 sample and rule | Ask 4 |
| R5 | hall B's throttle response (step-time inflation at each excess over contract) and each hall B run's mean inflation in 2027, from the excess rebuilt from the allocation record, the reservations' load and the research pool's response to it | missingness-measurement | hall B's five-minute meter, node states and the 2026 step logs (the draw as a line in the allocated nodes); the roadmap's blocks and the pool's share by reserved load | each run's inflation within 2.5 points | method shortcut: the pool at its 2026 mean share of the free nodes where its response to the reserved load was needed (the throttle on the rebuilt excess made right by reflex, R86) | R10 | Component 2 |
| R8 | each 2027 run's expected days from its window's start to its token budget | forecasting | R3 to R5, R10 and R11 on each run's config, budget, block and window; interruptions and works priced from the 2026 log and the work orders (made right by reflex, R87, R88) | expected days within 3 per cent | method shortcut: the hall B runs built without the pod penalty and with the pool at its mean share, so kide-8b-v4 fits and kide-34b-v3 is late and every hall B run is 4 to 13 per cent off | R3, R4, R5, R10, R11 | Ask 1 |
| R9 | the runs that will not finish inside their windows | synthesis | the reservation terms' test (expected finish inside the window) | exact set | unfinished chain: two members filed wrongly (kide-34b-v3 late, kide-8b-v4 fitting) with every other member right | R8 | Recommendation |
| R10 | the extra time a step takes when a job's nodes lie in both of hall B's pods, per cent, and which 2027 blocks do | investigation-loops | the 2026 node allocations (the node names carry the pod) against each run's steady step over the step its benchmark, mix and width predict; the roadmap's block column | within 2.5 points | dismissed own evidence: the node lists name the pod and the runs' residuals separate by it, the extra time filed as start-ups and drift | independent: allocations, step logs, benchmark | Component 1 |
| R11 | hall B's nodes the research pool keeps busy while the reservations hold 800 of its 1,024 (none), against light reserved load (its share of the unreserved nodes) | missingness-measurement | node states less the registry's held nodes, by the load the registered runs alone put on the hall through the fitted draw line, in 2026 | 800 reserved: none to 12 nodes | method shortcut: the pool at its 2026 mean share where the share depends on the reserved load | independent: node states, registry, meter | Component 3 |
| R12 | each 2027 run's finish, in days from 1 January 2027 | forecasting | R8 and the window's start | within 1 day | method shortcut: the hall B runs' finishes from the hurried days | R8 | Ask 1 |
| R13 | the 80 per cent range of each 2027 run's days | uncertainty | 160 draws of the 2026 record's own spreads (interruption counts and costs, the throttle fit, the works ratios, the pod penalty, the pool's light-load share) | range ends within 5 per cent | method shortcut: the hurried days' range | R8 | Ask 1 |
| R14 | each 2027 run's bridge from its benchmark days to its expected days, cause by cause (mix, slowest rank, padding, block across both pods, hall B, interruptions, works) | decomposition-attribution | the stated order in the answer blocks; each cause as measured above | each item within 0.35 days or 12 per cent | dismissed own evidence: the pod column left at zero and the hall B column carrying the pool at its mean share | R3, R4, R5, R10, R11 | Ask 2 |

Interruptions (the days each run loses to stops and restarts) and the provider works' days are columns of R14's bridge
and of the 2026 bridge, priced from the 2026 interruption log and the 2025-26 work orders by every careful run
(R87, R88), so they carry no result of their own.

Carry-forward: R1 stands alone on the allocation record and R2 on 2026's own records, so a run that slips in 2027
loses neither; R3, R4, R10 and R11 each stand on their own inputs and are graded run by run or figure by figure, so a
slip on one cause costs only that cause's cells and the verdicts it decides; R5, R8, R9, R12, R13 and R14 fall with
the causes they rest on, and only for the runs those causes reach (R10's error reaches kide-8b-v4, R11's and R5's the
hall B runs from February to April), so no one slip costs more than two of the eleven verdicts.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Attention cost quadratic in document length, with each step waiting for the slowest data-parallel rank | constructed by simulating the trainer's own cost and the synchronous step | no: every 2026 run carries it at its own size (overheads of 1 to 12 per cent in the profiled runs) | modelling: per-rank timings joined to the packing log, a cost model, then the maximum simulated at each 2027 run's own width and mix | modelling | keep (made right by reflex, R84) |
| Best-fit packing pads a mix with few short documents | constructed by simulating the loader's packing rule | no: the Q4 2026 extension runs pack under the same rule at 96 to 99.8 per cent | modelling: the rule replayed on the 2027 length sample | modelling | keep (made right by reflex, R85) |
| Hall B's contracted IT load below its full-load draw, with the provider throttling GPU power hall-wide past it | constructed by simulating the provider's power manager | no: every hall B job on 2026's capped days (123 days, excess up to 25 per cent) carries it | modelling: the excess rebuilt from the allocation record (the meter reads the cap), the response fitted, the 2027 load replayed | modelling | keep (made right by reflex, R86) |
| A job whose nodes lie in both of hall B's pods pays 22.0 per cent per step for the boundary | constructed by simulating the fabric: the gradient reduction crosses the spine between pods | no: the four 2026 runs across both pods (kide-70b-v1, kide-34b-v2, kide-34b-v1b and the scale test) carry it at 21 to 22 per cent, beside sixteen runs inside one pod that do not; in 2027 the plan's block sizes cannot tile two pods, so one block (kide-8b-v4) lies across | modelling and investigation: each run's steady step over the step its benchmark, mix and width predict, read against the node lists | modelling (a contrast read from four runs, then applied to the ledger's blocks); the split between the pods does not change it (256 and 128 nodes, 128 and 128, 256 and 256 run alike) | keep as a stump (P): it sits across the 2026 data, and a real fabric puts it on every straddling job |
| The research pool's admission falls as the load without it nears the contract (full share below 88 per cent of it, none from 97 per cent) | constructed by simulating the pool's scheduler | no: in every 2026 interval the registered load leaves the pool a share to take, 27 days with 768 nodes or more reserved show none and the months below 640 show 0.45 of the unreserved nodes | modelling: the pool's busy nodes from node states less the registry's held nodes, read against the registered load through the draw line | modelling | keep as a stump (Q) |
| Provider works run past their planned hours | constructed from the provider's work-order process | no: every 2025-26 major work order | a targeted comparison of planned against actual hours by type | routine once told | keep as a supporting step (made right by reflex, R88) |
| Row 6 cooling fault, September to October 2026 | constructed | no: every hall A job on row 6 nodes in those weeks; repaired before 2027 | a targeted query of per-rank timings by node | routine once told | keep as Layer 1 and a 2026 bridge item; no 2027 effect |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the GPU-days the 2026 runs held, all of 2026 | Missed | Right | Right |
| R2 the 2026 bridge from benchmark GPU-days to GPU-days held, by cause | Missed | Partly | Right |
| R3 each long-context 2027 run's slowest-rank overhead over its mean rank, per cent | Missed | Right | Right |
| R4 kide-34b-sci's packing fill | Missed | Right | Right |
| R5 each hall B run's mean step stretch in 2027 from the hall held to its contract, per cent | Missed | Missed | Right |
| R8 each 2027 run's expected days from its window's start | Missed | Missed | Right |
| R9 the runs that will not finish inside their windows | Missed | Partly | Right |
| R10 the extra time a step takes when a job's nodes lie in both of hall B's pods, per cent | Missed | Missed | Right |
| R11 hall B's nodes the research pool keeps busy while the reservations hold 800 of its 1,024 | Missed | Missed | Right |
| R12 each 2027 run's finish, in days from 1 January 2027 | Missed | Missed | Right |
| R13 the 80 per cent range of each 2027 run's days | Missed | Missed | Right |
| R14 each 2027 run's bridge from its benchmark days to its expected days, cause by cause | Missed | Partly | Right |
| Roughly | 0 of 12 | 4.5 of 12 | 12 of 12 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "a job whose nodes sit in both of hall B's pods runs about a fifth slower than the benchmark's idle slice"; rescues 1 of 12 results (R10; the pod cells of the bridges and the verdict on kide-8b-v4 stay
  with the pool's response and the other causes)
Pair estimate: 44.5 (measured by effort.py on the cut pack, every careful loss cited; quick 7.0, thorough 100.0)

## Stump factorial

Reflex route: every reflex set right (the hygiene battery on the logs; each run's benchmark days and the 2026
  GPU-days held reproduced; the slowest rank from the joined per-rank timings; best-fit packing replayed; hall B's
  excess rebuilt from the node states with the throttle fitted on it; interruptions priced from the stop log; works
  at the 2025-26 overrun record; blocks kept to their run's finish and a later run waiting for its nodes) and both
  stumps hurried (no pod penalty, the research pool at its 2026 mean share of the free nodes); it files kide-34b-v3
  late and kide-8b-v4 fitting, against the golden's seven late runs (120b-v1, 13b-code-lc32, 34b-16k, 34b-lc64, 34b-sci, 8b-lc64, 8b-v4)

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| P a job with nodes in both of hall B's pods pays for the boundary at every step, which the benchmark's one-pod slice cannot show | stump | no pod penalty: every block's step as the benchmark and the cost model give it | N09, N04 | six late: 8b-v4 fits; the block's 13.6 days of pod penalty gone | 34b-v3 late; kide-34b-v3 still late on the pool's mean share: the call stays wrong, rescues 1 of 12 | yes |
| Q the research pool backs off as the reservations near the contract, none from 768 nodes reserved | stump | the pool at its 2026 mean share of the free nodes | L15, N28 | eight late: 34b-v3 late; the pool's mean share adds 90 nodes of load in February to mid-March | 8b-v4 fits; kide-8b-v4 still fitting without the pod penalty: the call stays wrong, rescues 2 of 12 | no |
| S1 each step waits for the slowest data-parallel rank | reflex | (made unprompted) | R84 | - | - | - |
| S18 best-fit packing pads the scientific mix | reflex | (made unprompted) | R85 | - | - | - |
| S3 hall B's excess rebuilt from the node states, the throttle fitted on it | reflex | (made unprompted) | R86 | - | - | - |
| S4 works at the 2025-26 overrun record | reflex | (made unprompted) | R88 | - | - | - |
| J5 interruptions and restarts priced from the stop log | reflex | (made unprompted) | R87 | - | - | - |
| J6 each run's benchmark days and the 2026 GPU-days held reproduced | reflex | (made unprompted) | R90 | - | - | - |
| J7 a block extended to its run's finish, the next reservation waiting for the nodes | reflex | (made unprompted) | R89 | - | - | - |

Level: 4: two necessary stumps (P, Q), neither sufficient alone, their single drops on two distinct wrong late sets
  (kide-8b-v4 fitting; kide-34b-v3 late) and the reflex route on a third (both); the other stumps of the first
  draw are reflexes since the reviewer's audit run made them

## Open members

| Member | Opened by | Reflex route | Direct route | Golden |
|---|---|---|---|---|
| kide-120b-v1 | forced | right: late (1.24) | right: late (1.29) | late (1.140) |
| kide-13b-code-lc32 | forced | right: late (1.15) | right: late (1.06) | late (1.143) |
| kide-13b-lc32 | forced | right: fits (0.88) | right: fits (0.79) | fits (0.850) |
| kide-13b-v4 | forced | right: fits (0.92) | right: fits (0.76) | fits (0.857) |
| kide-34b-16k | forced | right: late (1.29) | right: late (1.05) | late (1.144) |
| kide-34b-lc64 | forced | right: late (1.17) | wrong: fits (0.71; no 2026 twin at that context and width, which the careful pass makes right by reflex, R84 to R86) | late (1.169) |
| kide-34b-sci | forced | right: late (1.15) | wrong: fits (0.85; no 2026 twin at that context and width, which the careful pass makes right by reflex, R84 to R86) | late (1.150) |
| kide-34b-v3 | Q | wrong: late (1.05) | right: fits (0.91; its twin kide-34b-v1-r2 ran unthrottled at the benchmark's rate) | fits (0.955) |
| kide-70b-v2 | forced | right: fits (0.84) | right: fits (0.82) | fits (0.840) |
| kide-8b-lc64 | forced | right: late (1.17) | wrong: fits (0.68; no 2026 twin at that context and width, which the careful pass makes right by reflex, R84 to R86) | late (1.177) |
| kide-8b-v4 | P | wrong: fits (0.94) | wrong: fits (0.82; the nearest 2026 run in hall B is a one-pod 8B ablation) | late (1.060) |

Direct route: each run's benchmark days over the realised rate (steady tokens per GPU-second over its benchmark's) of
  its nearest 2026 run in the same hall by model size, context and sequences per rank, read raw from the registry, the
  step logs and the benchmark; it files 120b-v1, 13b-code-lc32, 34b-16k as late (against the golden's seven) and so files kide-8b-v4 fitting (its
  twin is a one-pod ablation) and the long-context and scientific members wrongly (no 2026 twin at those contexts and
  widths), and kide-34b-v3 fitting like its twin kide-34b-v1-r2, which ran unthrottled: the 2026 record read at face
  value settles neither open member, and the reflex route's replay with the pool at its mean share files kide-34b-v3
  late
Margins: the honest family (twenty variants) moves no run's days by more than 2.3 per cent; kide-8b-v4 sits 6.0 per
  cent over its window with the pod penalty, 14.6 per cent under it without it and 5.9 per cent under it on the
  reflex route; kide-34b-v3 sits 4.5 per cent under its window, 5.2 per cent over it with the pool at its mean
  share: each margin is larger than the family's spread and smaller than its stump's worth

## Pinning list

| Constant | Home | Value the golden uses |
|---|---|---|
| hall B's node count | provider/service_schedule_S3_kaivola.pdf (S-3's table) and every row of cluster/node_states_2026.csv | 1,024 nodes (hall A 512) |
| each hall's contracted IT load | provider/service_schedule_S3_kaivola.pdf | 8,100 kW hall B (6,600 kW hall A) |
| GPUs per node | policy/compute_allocation_rules_CAR-2027-1.pdf section 6 and runs/run_registry_2026.csv (gpus) | eight |
| a window's span | policy/compute_allocation_rules_CAR-2027-1.pdf section 2 | 00:00 UTC on the start date to 00:00 UTC on the end date |
| a block's extension, the backfill after an early finish and a later run's wait for nodes still held | policy/compute_allocation_rules_CAR-2027-1.pdf section 2 | held to the run's finish, backfill to the window's end, the later run launches when the nodes are back |
| what counts as finishing and the committee's test | policy/compute_allocation_rules_CAR-2027-1.pdf sections 3 and 4 | real tokens, padding excluded; expected finish at or before the window's end |
| GPU-days held and benchmark days | policy/compute_allocation_rules_CAR-2027-1.pdf section 6 | nodes times eight times launch-to-final-checkpoint hours over 24; tokens over tokens per GPU-second over 86,400 |
| each run's block, rows and pods | plan_2027/roadmap_h1_2027.xlsx (block column) and the node names of runs/node_allocations_2026.csv | the rows the ledger names; a block lies across both pods when its node list names p1 and p2 |
| the 2027 works' planned starts and hours | provider/planned_works_h1_2027.pdf | as noticed, Helsinki local time |
| the checkpoint interval | every plan_2027/configs yaml (every_minutes) and the lost steps of runs/interruptions_2026.csv | 30 minutes |
| hall B's draw: kW with no node allocated, kW per allocated node | measured: provider/hall_it_load_2026.csv against cluster/node_states_2026.csv on the intervals clear of the contract; spread 0.07 per cent on any run's days across clear thresholds of 40, 60 and 120 kW and a floor of 600 allocated nodes | 1612.0 kW and 8.32 kW |
| the throttle response (stretch against the excess over contract) | measured: runs/step_log_2026.csv against the rebuilt excess; spread 1.34 per cent on any run's days across a quadratic, a straight line, a banded mean and a local baseline | 24.6 per cent at 20 per cent over |
| the pod penalty | measured: runs/node_allocations_2026.csv against runs/step_log_2026.csv; spread 21.1 to 22.1 per cent across the weighted, registered-only and per-twin estimates | 22.0 per cent |
| the research pool's light-load share and its back-off | measured: cluster/node_states_2026.csv less the held nodes of runs/run_registry_2026.csv, by the registered load through the draw line; spread 0.0 per cent on any run's days across a binned curve, a cut-off and a logistic curve and three light-load definitions | 0.446 of the unreserved nodes at light load, none at 768 reserved |
| the attention coefficient | measured: profiling/rank_step_samples_2026.csv joined to profiling/packing_manifests_2026.jsonl; spread 1.319 to 1.324 across run subsets | 1.324 |
| interruption rates, restart minutes and lost work | measured: runs/interruptions_2026.csv and provider/incident_log_2026.csv; spread 20 per cent either way holds the call | per node-day by hall, per run-day, per hall-day |
| the works overrun ratio by type | measured: provider/work_orders_2025_2026.csv; spread mean against median 0.0 per cent | 1.98 major, 1.07 routine |
| the first launch after a window opens | measured: runs/run_registry_2026.csv (launched_utc); spread no delay against the mean 0.35 per cent | about 37 minutes |
| document lengths by source and each mix's shares | data/doc_length_sample.csv and data/data_mixes.csv; spread another packing seed 2.3 per cent | the sample as filed |
| each configuration's benchmark rate | benchmark/tpbench_results.csv | as measured, tokens per GPU-second |

Variant battery: 15 variants of the hall B chain and its neighbours (the clear threshold at 60 and 120 kW, the draw
  line on 600 or more nodes, the contract at the meter's ceiling, the throttle as a line and as banded means, the
  stretch against local steady steps, the pod penalty from the registered runs and from each run's twin, the pool as
  a cut-off, a logistic curve and from three light-load definitions, the median works overrun, another packing seed,
  no launch delay), every variant files the same seven late runs and none moves a run's days by more than 2.3 per cent
  (kide-8b-lc64 on another packing seed); beside them five rivals of the cost model and the rates (the attention
  coefficient at its lowest and highest per-run fit, lengths from a fitted lognormal, a normal approximation to the
  slowest rank, hardware stops pooled over halls) and fourteen perturbations (each fitted input moved by its spread,
  the pod penalty by 4 points, the pool's light-load share by 0.1, the draw line's slope by 1 per cent) file the same call

## Data provenance

Source: generated by `generator/` from a simulated process: Saukko Labs' scheduler and trainer, its data loader's
  packing, the cluster's failures and restarts, the colocation provider's power manager, pods and works, the research
  pool's scheduler, and the 2027 roadmap with the provider's ledger of blocks
Behaves like the real thing: the trainer's step is the slowest data-parallel rank plus an exposed remainder (the
  synchronous all-reduce of data-parallel training, the straggler pattern ByteDance's OSDI 2025 study measured from
  sequence-length imbalance); attention cost follows the square of each document's length under document masking;
  best-fit packing without truncation pads as the 2024 packing studies report; GPU throughput falls with the power
  limit the way hall-level power capping behaves (Facebook's Dynamo, power oversubscription); a job whose ranks sit in
  both pods runs its gradient reduction over the spine between them at every step, as the pod-aware placement of
  large jobs assumes; the research pool's scheduler admits work against the hall's remaining headroom, so its load
  falls as reservations rise; interruptions arrive at node-level hardware rates with restart costs like the Llama 3
  report's; provider works overrun their plans
Genuine patterns: (1) throughput per GPU falls with model size and context length and rises with sequences per rank;
  (2) hall B's research pool follows a weekly cycle (busy weekdays, lighter weekends), a summer lull and a back-off
  near the contract; (3) node failure rates differ by hall; (4) every run shows a restart sawtooth of lost work since
  its last checkpoint; (5) loss falls along each run's own schedule (logged, unused by the call); (6) every run's
  step time wanders slowly (about one per cent) around its steady value
Problems by process: step counters reset at some resumes (a trainer logging fault in v2.3); the logger re-sends its
  last buffer after a restart (repeated rows); three runs renamed at a resume; provider files in Helsinki local time;
  meter intervals dropped during collector outages; GiB in the trainer and GB in storage; row 6's cooling fault; the
  hall handed back to the provider for works and facility events drops the whole hall's load
Breadth: fifty-three 2026 runs over two halls and 1,536 nodes, eleven 2027 runs, thirty-one files in five formats;
  choosing which of the step logs, traces, packing logs, meter readings, node lists and work orders carry each cause
  is itself the work

## Template check

Chain signature: assembly-reconciliation, decomposition-attribution, modeling, modeling, missingness-measurement,
  forecasting, synthesis, investigation-loops, missingness-measurement, forecasting, uncertainty,
  decomposition-attribution
Question form: which (which runs will not finish inside their windows), with how much (each run's days against the
  benchmark's)
Nearest build: (guard WARN on chains shared in shape or weight with task19, task2, task3, task4 and task9: none of
  them bridges a measurement to production at conditions never run, and the weight here is modeling against their
  assembly, measurement and synthesis) task24 (General Statistics, modeling weight, a set over a per-unit line on distinct wrong answers):
  its lessons are a QA any-miss product over objects, a pay floor's hinge and video track turnover in an
  annotation vendor's costs; here a maximum over parallel ranks, a packing process's fill, a capped meter's
  rebuilt excess, a job's place across two pods and a pool's back-off bridge a benchmark to production; the answer
  shape (a bridge against a forecast with drivers), the decision form and every mechanism differ. Abstraction
  sentence against it: none writable without naming the mechanisms, which share nothing

## Frontier check

Precedents: result 10 (the pod boundary) N09 (the topology assumed uniform over the history, here over the plan's
  blocks), N04 (a model's transfer to a new range named and left untested); results 5 and 11 (the pool's response) L15
  (a behavioural response assumed instead of measured), N28 (an input another process re-sets held at its latest
  supplied value); result 2 N09, L26 (a plausible shallower story passing its own checks: the residual filed as
  start-ups and drift); results 8, 9, 12, 13 and 14 inherit N09, L15 and L36 (a transfer fitted on the pilot's range
  carried to faster duties)
Shallow path checks: the reflex route back-tested on the 2026 runs reproduces their held GPU-days within 6 per cent
  run by run on the runs inside one pod and misses the three across both by their extra time, which a pooled
  benchmark-to-held ratio (1.236 over 2026) passes a leave-one-run-out check on because the straddlers' share of the
  GPU-days is a fifth (L37); the checks of another kind: each hall B run's steady step over its predicted step,
  split by the pods its node list names (1.00 against 1.21), and the pool's busy nodes against the registered load
  (a third to a half of the free nodes up to 640 reserved, none from 768), in two records at two grains
Assumption made false: "throughput measured in 2026 carries to 2027 at each run's FLOPs" (N04): the 2027 long-context
  runs pair heavier mixes with fewer sequences per rank and more ranks, the scientific run's packer pads, hall B is
  reserved past its contracted power for two months with a pool that backs off as the reservations near the contract,
  and one block lies across the pods the benchmark's slice sits inside one of, each tested in its own record (traces
  with packing logs; the length sample; meter with allocations and the registry; node lists with step logs)
Forcing: the line is each run's window; the golden keeps every forced run at 0.84 to 0.86 or 1.14 to 1.18 of its
  window and the two open members at 1.060 (kide-8b-v4) and 0.955 (kide-34b-v3); 20 variants and rivals of the hall B
  chain and the cost model file the same seven (120b-v1, 13b-code-lc32, 34b-16k, 34b-lc64, 34b-sci, 8b-lc64, 8b-v4), the shortcuts file another set (the benchmark alone, the
  reflex route, the full-context formula, the pooled 2026 ratio, the nearest 2026 twin, and each of the two stumps
  dropped alone) and each fitted input moved by its defensible spread (the attention coefficient, the throttle
  response, interruption rates and the works ratio by 20 per cent each way, the pod penalty by 4 points, the pool's
  light-load share by 0.1, the draw line's slope by 1 per cent) leaves the late set unchanged; the world's own replay
  files the same seven with every run's days within 4 per cent (asserted in `checks.py`)
Noun swap: nearest by `skeleton.py check` is task7 arch 11 (severity none): its decision form (one of a few options)
  and answer pattern (no single correction clears) differ, its lessons share non_additive_aggregation only through a
  seasonal coincidence of chargers, its mechanisms, detection and file roles do not carry; task24 (severity none)
  shares the lesson key and the common pattern, nothing else
Closed strategies: the call turns on P (position_on_network_effect, a job's place across two pods) and Q
  (behavioural_response_measured, a pool's admission as the reservations grow), both open ground; the nearest closed
  cards are "spillover" (no treated-control comparison is contaminated: the penalty is the job's own, read from the
  jobs that lay across the boundary), "composition" (the pool's share changes with the reserved load, not with a mix
  of units) and "transport to a new mix" (no population is re-weighted); the slowest rank, the padding and the capped
  meter stay as results made unprompted, and no closed lesson is kept even as a supporting step (the row 6 fault and
  the works overrun are Layer 1 and a supporting step on open ground)

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
| SF11 | a block lying across both pods | any node of the block in each pod; the pod holding most of its nodes; a share of its nodes in the second pod | any node in each pod, the penalty whole | the 2026 straddlers' penalty does not move with the split (256 and 128, 128 and 128, 256 and 256 nodes run alike); kide-8b-v4's block is 32 and 32, a tie a majority rule cannot read; same call |
| SF12 | a later reservation on rows an earlier one held | launches when its window opens; waits for the nodes to be handed back | launches at the later of the two | CAR-2027-1 section 2; no block shares rows with an earlier run inside its window and the earlier run's slowest of the world's replays, so the rule never binds (asserted) |
| SF13 | the pool's busy nodes in the 2027 plan | its 2026 mean share of the free nodes; its share by the reserved load; none | by the reserved load, through the fitted draw line | node states less the registry's held nodes show both regimes in 2026; the three readings file different sets and the measured one is the golden |
| SF14 | hall B's draw | a line in the allocated nodes; a line in the registered and the pool's nodes apart | one line in the allocated nodes | every node left idle or down draws the same, so the line is the whole of it (the two lines coincide to 0.1 per cent); same call |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the 2027 runs are the roadmap's rows; the 2026 population is every run launched in 2026 (data dictionary); C1 for the verdicts |
| 2 | Unit of account: a run; days and GPU-days named in the asks; C4 (GPU-days against days differ by a run's node count) |
| 3 | Attribution window: a window runs 00:00 UTC on its first day to 00:00 UTC on the day after its last; no run starts off a day boundary; a block's rows are held to its run's finish and a later reservation on the same rows waits for them (never binding) |
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
| 21 | Clause scope: the reservation terms apply to every 2027 block; the backfill clause to reserved blocks only; the wait clause to blocks that share rows |
| 22 | Forward window contents: the 2027 roadmap (runs, blocks and their rows, windows, budgets), configs, length sample, works calendar and the pool's 2026 response as the shipped drivers for 2027 |

## Literal reader

The prompt asks which 2027 runs will not reach their token budgets inside their reserved windows and how many days
each will take against the benchmark; the reservation terms define the window, finishing, the extension of a block
to its run's finish, the wait of a later run on the same rows and the test; they define GPU-days held and the 2026
population. Executed word for word, each run's days are the wall-clock days to its budget under the conditions the
files describe, and the late set is every run whose expected finish falls after its window; no filed sentence states a
cost model, a packing fill, a throttle, a pod penalty, a pool's response or an overrun, so every literal reading needs
the same estimates and none files a different verdict. The roadmap's block column files where each block lies; it does
not say what lying across two pods costs.

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
- 2026-11-14, the reviewer's audit of architecture 1 (`runs/holistic_audit_2026-11-13.md`, pasted by the author): three findings. Determinism not pinned: the hall B stretch chain rested on a fitted would-be draw biased by a per-model draw (0.93 to 1.02) and a pool factor of 0.95 that the world set and no file held, and the audit run's method gave 17.7 days of throttle on kide-120b-v1 against 13.47. A graded figure infeasible: the reserved blocks filled hall B's 1,024 nodes from 22 February and kide-34b-v3's extension to about 16 March collided with kide-13b-v4's 15 March launch (1,152 nodes), with no precedence between "launches when its window opens" and the extension. And the audit run reached the same seven late runs, so every move of the draw's stumps (S1, S18, S3, S4) was a reflex (R84 to R90). Repaired in place: one draw per node, hall-level stops that idle the hall, the pool's admission against the contract, a pod penalty for jobs across hall B's two pods, a ledger of blocks by rows with no block sharing rows inside its window and a stated wait for nodes still held, a variant battery of twenty rivals and fourteen perturbations, and the two new stumps (P, Q) opening kide-8b-v4 and kide-34b-v3; the call is still seven of eleven late but with a different seven.
- 2026-11-14, at the repair: a per-model draw per node (a published utilisation by size) as the throttle's stump: the client's closed composition card, and the mix changes only the intercept the draw line already fits; dropped.
- 2026-11-14: a neighbouring pod's load slowing a job through shared spine capacity: the client's closed spillover card; dropped.
- 2026-11-14: a trainer release changing the step by about three per cent from 1 August: a break built into the data that one cross-tab shows and one dummy fixes (banned item 4); dropped.
- 2026-11-14: one slow rack in hall B: a defect only in the units that decide the answer; dropped.
- 2026-11-14: a successor's deferral behind a late block (the audit run's own catch) as a stump: a ledger conflict is caught by reflex (R89), so the ledger is made feasible by construction and the rule filed; dropped as a stump.
- 2026-11-14: a filed cap change or contract amendment for 2027 as the new throttle's stump: filed is executed; dropped.
- 2026-11-14: the throttle applied per pod (each pod on its own busway): the pool's nodes by pod are unrecorded, so the per-pod loads and the golden's figures would be unpinned; dropped.
- 2026-11-14: a spare node taken from the other pod after a hardware fault (a job becoming a straddler mid-run): every large run would straddle within days, which no operator accepts; the spare is drawn from the failed node's pod.

