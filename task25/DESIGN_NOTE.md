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

## Tried and rejected

- 2026-11-13, at the draw, before this world: an object store's 2027 durability by pool (latent sector errors under a fill-stretched scrub cadence, rebuilds slowed by concurrent rebuilds, racks sharing a power feed): two of its three deciding steps sit on the client's closed common-shock card, data-loss rates are rare-event figures too wide to force a set, and the setting is the client's triage example and storage strategy; dropped.
- 2026-11-13: a nightly data-pipeline SLA forecast (merge bias at DAG joins, skewed joins, executor queueing): a careful run simulates the DAG by reflex and queueing at shared slots sits next to the closed shared-resource card; dropped.
- 2026-11-13: an LLM-judge evaluation with differential misclassification by checkpoint: the runs' own field, judge-bias corrections are a reflex there, and its other steps (contamination, transport to traffic) are a planted defect and a closed card; dropped.
- 2026-11-13: a scaling-law loss forecast for a larger run (schedule-matched endpoints, repeated data, a downstream sigmoid): every step is published method the runs apply by reflex, and the training-run setting is the client's worked illustration and its machine-learning strategies 1 to 4; dropped.
- 2026-11-13, at the draw: the run's analysis type as Forecasting (BLOCK, ban.pairing against task24's General Statistics x Forecasting); drawn as Comparative Analysis & Explanation, which the bridge from benchmark to production is.
- 2026-11-13, at the draw: cross-pod gradient reduction and hot-spare exhaustion as stumps (dropped, see the screen); the row 6 cooling fault and the works overrun kept only as supporting steps.
