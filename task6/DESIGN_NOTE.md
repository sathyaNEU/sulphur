# task6: Rotalinha's internal services over their 2026 latency error budget (architecture 7, repaired after the determinism return of 2026-11-22)

## Draw

The design of architecture 6 (the single deep step it was returned for) is in git history at commit bd3bbed, and
architecture 7 as approved on 2026-11-11 and returned on 2026-11-22 at commit 458d644.

Subdomain: General Statistics & Data Science, missing data, censoring and measurement error
Analysis type: Descriptive & Distribution Analysis (where each service's December latency share really sits, once the
  sample's design weights, the December hours the trace export no longer covers and the incident time charged
  elsewhere are handled)
Answer shape: a flagged set with the evidence: the services over budget with each SLI, its interval and the December
  incidents' root causes behind it, in the order their engineers start
Weight: a hard-to-measure quantity: each service's share of slow requests, from a whole-trace sample whose inclusion
  probability is recorded nowhere, a span export that no longer covers the month's first 274 hours, a coarser record
  that does, and incident time charged to the service that owned each root cause. The last builds leaned on
  attribution (task13), robustness (task2) and forecasting (task12).
Data-native sentence: the trace store keeps whole traces at the edge, a fixed number an hour per edge service, so
  every internal service's kept spans carry the keep shares of the several edge services that call it; it keeps
  spans for 31 days and its hourly duration histograms for thirteen months, so by the January pull December's first
  eleven days survive only as bucket counts with no trace to join them; and December's incidents were faults in one
  service's own handling that reached the services calling it, at the evening peaks when every service is already
  slower with load, named by the responders in the order they suspected them.
People: Teresa Nogueira (Head of Platform Reliability), Bruno Marques (FinOps), Ivo Pereira (SRE): the personas drawn
  for architecture 5's world and kept with it.

- **Card.** `.claude/skills/fingerprint/cards/task6.json`, architecture v7, registered 2026-11-09T16:23:04Z. This is
  a repair of that registered design after a determinism return, on the reviewer's direction to keep the weighting
  and the dated causes: the card's registration stands and its driver, stump, results and skeleton are brought up to
  the repaired third judgment. The sections the harness added after 2026-11-09 are written below where they apply;
  `generator/core.py` is not built (see Tried and rejected).
- **Decision.** Which internal services ran over their 2026 latency error budget; each gets a reliability engineer
  for January to June 2027, the one whose SLI counts the most requests over its threshold first. Retrospective by
  design: the SLO year closed on 31 December 2026 and the programme starts in January.
- **Deliverables.** A short written review and a CSV, as the approved prompt had them: a repair keeps the prompt's
  files (`guide-to-prompt` section 2), and the annual reliability review is a written review to the engineering
  leadership group by the standard's own section 5.
- **What the return found (2026-11-22).** Determinism (main) failed, every other check passed, reward 45.0:
  journey-search's verdict turned on how the 274 hours before the export were filled, and nothing shipped settled it.
  Reproduced on the shipped pack before anything was changed (pipeline.json `returned`).
- **What was changed, and why not the reviewer's two fixes as written.** Shipping the early spans leaves a union of
  two exports; moving journey-search clear of every load fill leaves every SLI's accepted range as wide as the fills
  disagree and takes the judgment out. Instead the record now holds the deciding configuration: the tracing store's
  span metrics (an hourly duration histogram of every span it ingested, kept for thirteen months) cover the whole of
  December. The early hours are measured, not extrapolated: exactly where a service's threshold is a histogram
  boundary (five services), and by splitting one bucket where it is not (five services). Every service is placed so
  that no split of that bucket, straight-line interpolation or either of its bounds moves the list.

## Stump screen

Written for the repair on 2026-11-25, before the generator was touched. The weighting and the dated causes are the
reviewer's kept steps; the candidates are for the third judgment.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| the hours before the export filled from a model of load on the held hours (architecture 7 as shipped) | the early hours ran at the held hours' share at the same load (N10, L34) | none: no record holds the early hours | 10 (the run's alternative is not ruled out by named data), 16 (no referee), 11 | dropped: the returned fork |
| the early spans shipped as a second export | none | the second export | 2 (a union is a reflex), 4, 14 | dropped |
| a load balancer latency statistic per service and hour | the kept spans stand for the service's requests (L08) | the balancer's own latency, all requests | 18 (it scores the weighting of every internal service) | dropped: it hands the first judgment over |
| a weekly pull of slow traces only | the kept-root count of an early hour is the sampler's target | the sampler's rule recovered from the held hours | 13 (its remedy is the first judgment's weights again), 9 | dropped |
| the store's span metrics on the SDK's default boundaries, whole December, by service and span name | a second record at another grain set aside because it has no trace identities (N27); the level read off the detailed record whose coverage ended (L44); a bucket split by straight-line interpolation (the tool's default) | the held hours, where the export and the span metrics count the same spans: the split is measured there | none (18: the overlap scores the split, which is why the split is a banded figure and never moves a verdict) | kept |

## Deep reasoning

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), serving Descriptive &
Distribution Analysis: a population share estimated from a sample whose inclusion probability is set by another unit
and recorded nowhere, which covers only part of the population's period at span grain and all of it at a coarser
grain, with part of the population left out by a filed rule whose membership has to be established.
Domain test: the field's own estimators for a share from a stratified cluster sample with unequal, unrecorded inclusion
probabilities (Horvitz-Thompson or Hajek, each trace weighted by its root edge service's hourly keep share), a
quantity recorded at two grains bridged by the conditional distribution the finer record shows (interval-censored
durations split at a threshold inside a class), the design-based variance of the combined ratio, and a changepoint
on load-adjusted residuals to date which service's own handling degraded first.
Swap: "which hospital wards ran over their waiting-time budget" breaks at once: a ward has no trace root whose keep
share sets every other ward's inclusion, no call tree that makes one ward slow because another is, and no store that
keeps a month of visits and a year of histograms.
Where the weight sits: the hard-to-measure quantity, every service's December SLI. The kept spans are a cluster sample
drawn at the edge, so four internal services carry their callers' keep shares (partner-gateway, fares and
notifications up, payments down); a third of December's requests have no spans, only bucket counts by service and
span name, which have to be weighted by callers they do not name and split at a threshold five services' buckets do
not carry; and the incident time PR-SLO-3 3.2 leaves out depends on a root cause no review has recorded yet. The work
is long because each piece has its own evidence, not because one piece is clever.
Layer 1: re-sent span rows from the exporter's retries (the same span id twice; the span metrics count each span
once); traces begun in the hour before the export whose root the store had dropped; the span metrics' rows split by
status code and cumulative by boundary, with no row for a series' empty hour; the balancer's target groups renamed
on 1 July (the catalogue's crosswalk); the status page in Lisbon local time against the incident tool's UTC; the
incident export's final service lists against the timeline's add times; 404s, 5xx and a retried partner-gateway call
counting as requests. None moves a graded result except the incident minutes, which grade the timeline
reconciliation itself.
Not one thing: three judgments each move the list, and each alone leaves it wrong. Without the trace roots' weights
the list is places and seat-map; without the dated causes it is partner-gateway, places, journey-search and seat-map;
without the hours before the export it is six. The intervals, the minutes, the shares and the bucket's split each need
their own work.
One-fact test: on the careful pass (own hourly counts, each incident on the service furthest over its curve, the
export's hours), "each kept span counts at its trace root's hourly keep share" leaves the list at partner-gateway,
places, journey-search and seat-map; "the store's span metrics hold the hours before the export" leaves it at places,
journey-search and seat-map; "the earliest rise owns the cause" leaves it at places, fares, journey-search and
seat-map (effort.json, measured).
Not semantics: every field, unit and clause read correctly (the re-sent rows, the windows, the halves, the zones, the
cumulative buckets) still leaves the own-hour weighting at partner-gateway 1.0, fares 0.9 and notifications 0.7 and
the export's hours at journey-search 1.1.
Not rule application: PR-SLO-3 files what an SLI is, that a request counts whether or not the store kept a span, which
incident time leaves it and what owning a root cause means; no filed rule weights a span, says the export is short,
names the span metrics, splits a bucket, dates a degradation or builds an interval.
Estimand: PR-SLO-3 3.1 (December in Lisbon time), 2.1 to 2.4 (every request a service handled, kept or not, its server
span's duration, by the time it started, errors counting), 3.2 (incident time from when the tool added the service to
when the status page showed every component operational, left out unless the service owned the root cause), 3.3 (a
service owns it when the failure was in its own handling, systems outside the catalogue included; a service that slowed
only because a catalogue service it called slowed does not), 3.4 (a breach is the SLI over the budget), 5.2 and 5.4
(the minutes, the halves).
No decoy: no memo, draft or stakeholder figure; the capacity review and the app reviews are context the golden never
reads; the closed reviews record causes only for January to November, and nothing names December's; no shipped
sentence mentions the store's retention or says what the span metrics are for.
No replay: no shipped figure is re-derived; no stated number is wrong.
Pinned: every rival estimator on every SLI lands on the same one-decimal value in the held hours (Horvitz-Thompson, the
span's own hour, the orphans dropped). For the hours before the export, five services are counted exactly (their
threshold is a histogram boundary); for the other five, every split of the threshold's bucket the held spans support
(one pooled share, two to thirty bands of hourly load, a logit in load, the hour of day, weighted or not) gives the
same list, the same order and SLIs within 0.07 of each other, which is each figure's stated range. Straight-line and
log-linear interpolation inside the bucket and the bucket's two bounds give the same list and other figures; on the
held hours, where the spans say what the bucket holds, interpolation rebuilds 1.6 to 3.0 times the over-threshold
requests, so it is ruled out for the figures by the files. Fills that read no span metrics (a flat share, a match on
the hour, two or three load bands) put journey-search over and partner-gateway at 2.8 to 3.0, where the span metrics
count partner-gateway at 2.3 with nothing estimated. The onset rule (one sustained changepoint, a rise of 2.2 times) fires on 3 of 54
placebo windows, and every rival detector calibrated the same way names the same seven owners or sees nothing. The trace bootstrap with the splits refitted lands within 0.02 of the linearised interval.
Run forecast: a strong run loses R3, R5, R7 and R8 by method shortcut (each service's own spans reweighted on its own
hourly count, as the run on file did); R4 and R5 by a method shortcut of another kind (the export's hours read as
December, the uncovered window filled by a same-hour match, or the span metrics opened and their buckets interpolated);
a weaker run also stops at the first story on R2 (the 14, 21 and 26 December incidents on seat-map, journey-search
and accounts); R6 falls to a method shortcut (a binomial interval); R1 is earned.
Strategy label: WORKS IN FORM (variance and inclusion that the sample's design sets, and missingness by design, from
`sulfur-strategies.md`'s clean comparison and heterogeneity rows read as results) for the weighting and the two
grains, and the client's own investigation shape for the attribution (dating onsets to separate cause from symptom).
Depth level: 5 on the client's scale. Three judgments that each move the list and each need estimation (the trace
roots' weights, the hours before the export measured at another grain, the causes dated by own handling against load),
a fourth with its own figure (the design-based interval), and seven distinct wrong lists from seven shortcut routes.
Lesson: an estimate from a sample drawn somewhere else, kept at two grains over two horizons, must carry that sample's
design through both records (weights from the trace root where there is a trace, from the callers' mix where there is
only a count; a threshold inside a class split by what the finer record shows), and an incident's cause is the
earliest degradation once load is taken out; no build on file pairs a design-weighted share across two grains with
dated causes.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each service's customer-facing incident minutes in each half of 2026 | Assembly and reconciliation | PR-SLO-3 5.2 and 5.4; the timeline's add times; the status page's last operational change | exact | narrow look at broad data: the export's final service lists read from each declaration, or the tool's resolve time as the end | - | Ask 4 |
| R2 | the service that owned the root cause of each December customer-facing incident | Investigation loops | PR-SLO-3 3.3; own handling time against a load curve on the export's incident-free hours; the earliest held rise | exact | stopped at the first story: the service named first, or the one furthest over its curve across the whole incident (14, 21 and 26 December on seat-map, journey-search and accounts) | R1 | Component 2 |
| R3 | the service that starts first, and payments' December SLI | Missingness and measurement | each span at its trace root's hourly keep share (the root's RequestCount over the roots kept that hour) | exact (the first to start); payments 0.2 at one decimal | method shortcut: each service's own spans on its own hourly count (places first; payments 0.5) | independent: the kept traces' roots and the balancer's counts | Component 1 |
| R4 | places' and booking's December SLI | Data discovery | PR-SLO-3 2.2 and 3.1; the span metrics' counts for the 274 hours before the export; places' bucket split at the share its held spans show | places 1.37 to 1.45; booking 0.3 exact | method shortcut: the export's hours read as December (1.7 and 0.5), or the bucket interpolated (places 2.0) | independent: the span metrics and the export's first span | Component 3 |
| R5 | every service's December latency SLI | Missingness and measurement | R3's weights through both records, R4's hours, the windows R2 leaves out | exact at one decimal for the five boundary services; the split family's range for the five bridged | method shortcut: own hourly counts, the export's hours, the whole-window causes | R2, R3, R4 | Ask 2 |
| R6 | a 90 per cent confidence interval on each over-budget service's SLI | Uncertainty | the trace store's design: strata of root service and hour, whole traces as units; the early hours' own sampling error and the split's | each end within 0.03 (linearised against bootstrap) | method shortcut: a binomial interval on the kept spans, 0.03 to 0.05 too narrow at one end for the internal services and right for the edge ones; on the reflex route every interval sits on a wrong SLI | R5 | Ask 1 |
| R7 | the services over budget | Synthesis | PR-SLO-3 3.4 on R5 | exact | method shortcut: the SLIs on own counts (partner-gateway, fares and notifications within), from the export's hours (journey-search over) or with the whole-window causes | R5 | Recommendation |
| R8 | the start order, each one's share of the over-threshold requests the SLIs count, and the requests beyond budget | Decomposition and attribution | R5's weighted numerators and counted requests | order exact; shares within a point; 190,000 to 220,000 | method shortcut: shares of the kept over-threshold spans on the own-hour weights over the export's hours | R5, R7 | Ask 1 |

Carry-forward: R1 stands alone (the incident records only). R2 needs only R1's windows. R3 falls with the weights
alone, R4 with the early hours alone, R2 with the dating alone: each judgment owns one component. R5 to R8 sit
downstream of all three: every internal service's SLI falls with the weights, fares', notifications',
journey-search's and accounts' with the dating, and eight of ten SLIs, every share and the requests beyond budget
with the early hours.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| whole traces kept at the edge, a near-fixed 60 an hour per edge service | constructed (the world's sampler) | no: it moves all four internal services (fares, partner-gateway and notifications up, payments down), every interval and both records | a targeted query: each kept span's root against the balancer's hourly counts | a reweight by the root's keep share where there is a trace; where there is only a count, the callers' mix has to be built from the client spans | keep, one judgment of three |
| the store's 31 days of spans against thirteen months of span metrics: the export begins at 12 December 10:00, a third of December's requests without spans | constructed (the store's retention and the review's pull date) | no: every service loses the same hours, and eight of ten SLIs move by a tenth or more (journey-search 1.1 to 0.8, places 1.7 to 1.4, partner-gateway 3.1 to 2.3) | one look at the export's first span; the span metrics' first row | modelling for five services: a threshold inside a bucket, split at the share the held spans show, weighted by callers the counts do not name; a count for the other five | keep |
| the span metrics' boundaries against the thresholds: five thresholds inside a bucket | constructed (the SDK's default boundaries, the standard's round thresholds) | no: journey-search, fares, places, accounts and notifications, two of them within budget and three over | one look at the header | modelling: the bucket's split, measured on the held spans and carried by load | keep; decides no verdict (asserted) |
| December faults in one service's own handling (2.6 to 3.9 times its handling time), reaching the services that call it | constructed (seven incidents in six services) | no: nine services named, faults in six, one incident on a single service | modelling: own handling time against a load curve, a changepoint per span name | modelling | keep |
| callers' workers waiting on a slow call late in an incident, in three incidents further over their curves than the fault | constructed (five of seven incidents; ramped, uneven onsets) | no: journey-search, seat-map, booking and accounts; the larger-than-the-fault form in INC-1579 (decides no verdict), INC-1611 and INC-1619 (fares, notifications and journey-search) | modelling: onset order, not size | modelling | keep |
| evening, holiday and campaign load raising every service's handling time | constructed (the world's queueing curve, the Christmas weeks, two campaign evenings) | no: every service, every day | modelling: the load curve itself | modelling | keep |
| the exporter re-sending a batch | constructed (one batch in three hundred) | no | a query: a repeated span id | routine | keep, texture (moves nothing) |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 incident minutes by half | Missed | Right | Right |
| R2 root cause of each December incident | Missed | Partly | Right |
| R3 the first to start and payments' SLI | Missed | Missed | Right |
| R4 places' and booking's December SLI | Partly | Missed | Right |
| R5 every service's December SLI | Missed | Missed | Right |
| R6 the 90 per cent intervals | Missed | Missed | Right |
| R7 the services over budget | Missed | Missed | Right |
| R8 start order, shares, together, beyond | Missed | Missed | Right |
| Roughly | 0.5 of 8 | 1.5 of 8 | 8 of 8 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (each pass's methods run end to end on the cut
pack by generator/analysis.py: quick unweighted with the first-named service at fault, the export's hours alone and the
export's lists from each declaration; careful the reflex route, each service's own hourly count, each incident on the
service furthest over its load curve and the export's hours read as December, with binomial intervals; thorough the
golden).
Largest single hint: each kept span counts at its trace root's hourly keep share; rescues 1 of 8 results
Pair estimate: 24.8
Clean-data test: with every file de-duplicated, re-keyed and read correctly, the reflex route still files places,
journey-search and seat-map, by an analysis a careful analyst would call reasonable: hourly reweighting to the
balancer's counts, causes by the size of each service's excess over its load curve, and the month read from the
export.

## Stump core

No `generator/core.py`: the card predates the core rule. The figures below are printed by `analysis.py` on the cut
pack (`Golden.run()`: `lattice`, `family`, `naive`, `loadfill`, `bridge_check`) and written to `effort.json`.

Unobserved part: each service's requests over its threshold among all the requests it handled in December. No record
holds it: the export holds a sample of whole traces from 12 December 10:00, kept at each edge service's hourly rate;
the span metrics hold the same sample for the whole month as bucket counts by service and span name; the balancer
holds every request and no duration.
Instruments: the span export (exact durations, the trace and its root; blind to the first 274 hours; read raw on own
hourly counts it files places, fares, journey-search and seat-map with the dated causes); the span metrics (every
hour; blind to the trace, the root and any duration inside a bucket; read raw with own counts and interpolated
buckets they file other SLIs for five services); the balancer's hourly counts (every request; no latency); the
incident tool, its timeline and the status page (who was named when; no cause for December).
Referee: the export's own hours, where the span metrics and the spans count the same requests. The golden's split
rebuilds the held hours' over-threshold requests exactly in sample; straight-line interpolation rebuilds 1.9 times
journey-search's, 2.3 times fares', 3.0 times places', 1.6 times accounts' and 1.7 times notifications'. It is a
calibration set for the split and nothing else: it scores neither the weights nor the causes, and the early hours'
loads are lighter than most of it, which is why the split is carried by load and banded.
Strongest standard route: for partner-gateway, fares and notifications, post-stratification of each service's own
spans to its own hourly RequestCount with a bootstrap (1.0, 0.9 and 0.7 against 2.0, 1.0 and 1.0): its totals
reconcile to the balancer hour by hour by construction, and only the trace roots' kept counts show the mix is wrong.
For journey-search, the export's hours with any fill fitted on them (1.1 on the hours themselves, 1.0 to 1.2 from a
flat share to four load bands): refuted by the span metrics' counts for the early hours.
Said out loud: "each kept span stands for the requests of the edge service that started its trace" leaves the roots
to link, the hourly keep shares to build, the early hours' series to weight by callers the counts do not name, and
the intervals. "The store's span metrics cover the hours the export lacks" leaves the series to weight, five buckets
to split and the split to measure and carry by load. "The earliest rise owns the cause" leaves own handling time to
separate from the calls waited on, the load curve, the changepoint and its calibration.
Worth: the weights on partner-gateway 1.28 points (2.29 against 1.01) over a family spread of 0.00; the dated causes
on fares 0.55 (1.30 against 0.75) over 0.04 and on notifications 0.38 over 0.03; the early hours on journey-search
0.33 (0.81 against 1.14) over 0.07.
Regimes: second and third stump: the weights open partner-gateway, the dated causes fares and notifications (and put
journey-search over), the early hours journey-search.
Sharp: the weights' wrong route passes its own check (hourly totals reconcile to the balancer) and its evidence is in
the roots' kept counts; the dating's wrong route names the service with the largest excess, which a plot confirms,
and its evidence is the order of the rises; the early hours' wrong route reads a complete-looking export and its
evidence is the first span's time against the span metrics' first row. Each correction differs across members
(partner-gateway up and payments down; three incidents of seven; five services exact and five split) and each owns a
graded figure (R3, R2, R4).
Earns: effort.py's table above; the reflex route keeps R1.

## Stump factorial

Reflex route: every file read and cleaned, the spans de-duplicated, each service's own spans reweighted hour by hour
on its own RequestCount, every incident window left out by the timeline's add times and the status page's end, each
December incident put on the named service furthest over its load curve across the incident, December read from the
hours the export holds: places, journey-search and seat-map. This route is the careful but hurried pass.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| J1 each kept span at its trace root's hourly keep share | stump | each service's own spans on its own hourly count | L08 | places and seat-map | partner-gateway, places, journey-search and seat-map; rescues R3 | no: one reweight in the export, a caller mix to build in the span metrics |
| J2 each December incident on the service whose own handling rose first | stump | the service furthest over its load curve across the incident | L26 | partner-gateway, places, journey-search and seat-map | places, fares, journey-search and seat-map; rescues R2 | no |
| J3 the 274 hours before the export counted from the span metrics | stump | December read from the export's hours | L34, N27, L44 | the five and journey-search | places, journey-search and seat-map; rescues R4 | no: a count for five services, a bucket to split and series to weight for five |

Level: 5: three necessary stumps, none sufficient, the single drops on three distinct wrong lists and the seven
shortcut routes on seven.

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| partner-gateway | 2.29 against 2.0 (over by 0.29; interval 2.17 to 2.41) | 0.00 (its threshold is a boundary) | 1.33, within | 0.67 unweighted, within | J1 |
| fares | 1.30 against 1.0 (over by 0.30) | 0.04 | 0.47, within | 0.42, within | J1 and J2 (0.88 without the weights, 0.75 without the dating) |
| notifications | 1.30 against 1.0 (over by 0.30) | 0.03 | 0.56, within | 0.56, within | J1 and J2 (0.68 and 0.92) |
| journey-search | 0.81 against 1.0 (within by 0.19) | 0.07 | 1.65, over | 0.90, within for the wrong reason | J3 and J2 (1.14 without the early hours, 1.16 without the dating) |
| payments | 0.21 against 0.5 | 0.00 | 0.52, on its line | 0.40 | forced as a verdict; its figure is J1's own |
| places | 1.41 against 1.0 | 0.05 | 1.70, over | 1.03 | forced as a verdict; its figure is J3's own |
| seat-map | 1.93 against 1.0 | 0.00 | 2.54, over | 1.83 | forced |
| booking | 0.33 against 0.5 | 0.00 | 0.46 | 0.30 | forced as a verdict; its figure is J3's own |
| tickets | 0.72 against 1.0 | 0.00 | 0.68 | 0.66 | forced |
| accounts | 1.22 against 2.0 | 0.03 | 1.78 | 1.69 | forced |

Direct route: the kept spans' own share over each threshold, unweighted, with the first-named service at fault and
the export's hours (the quick pass in `analysis.py`): seat-map alone. It lands wrong because the kept spans are a
fixed number an hour whatever the traffic.

## Data provenance

Source: generated by task6/generator from a simulated platform (seed 2711): hourly traffic for six edge services, the
calls each request makes to four internal services, queueing latency under load, an edge sampler keeping about 60 whole
traces an hour per edge service, a tracing store that keeps spans for 31 days and derives span metrics from every span
it ingests, and December's incidents as faults in one service's handling.
Behaves like the real thing: latencies are log-normal with a queueing curve in each service's hourly load, as service
latency is; the sampler is head-based and per trace at the edge, as OpenTelemetry's rate-limiting samplers are; the
store deletes whole hours of spans past its retention, as block-based trace stores do, while the metrics it generates
from spans live in a metrics store with a longer retention, on the SDK's default histogram boundaries, cumulative and
split by status code; callers inherit their callees' slowness and queue behind them late in an incident, as
thread-pool services do; responders name the paging service first and add the cause as they find it.
Genuine patterns: (1) diurnal peaks per service and a weekend dip (2) December seasonality: a quiet first fortnight,
the Christmas weeks and two campaign evenings (16 and 28 December) (3) queueing under load, steepest for partner-gateway
(4) per-operation latency that differs by caller (5) incidents that start before they are declared and end after
mitigation (6) a retried partner-gateway 5xx.
Problems by process: the exporter re-sends a batch (repeated span ids); the store's retention leaves the export
starting at 12 December 10:00, with orphan spans of traces begun in the hour before; the span metrics are cumulative
by boundary, split by status code and silent for a series' empty hours; the balancer renamed its target groups on 1
July; the status page writes Lisbon local time and the incident tool UTC; the tool's export carries each incident's
final service list while the timeline dates each addition; December's reviews were still open on the export date.
Breadth: ten services, 744 December hours (470 of them in the export), 723,137 span rows across 174,122 traces,
29,330 span-metrics rows over 35 series, 44,160 hourly balancer rows, 87 incidents with 581 timeline events and 41
status posts, so choosing what to read and at what grain is work.

## Template check

Chain signature: assembly-reconciliation, investigation-loops, missingness-measurement, data-discovery,
missingness-measurement, uncertainty, synthesis, decomposition-attribution
Question form: which, then how much and how sure
Nearest build: task13 (an outage record and a ranked list of feeders by modelled exposure); the nearest chain on file
dates no cause and weights no sample. The abstraction sentence a reviewer would write for task6 and task13 ("rates
read through a model of exposure") does not hold: here the weights come from a sample's design, the early period from
a second record at another grain and the exclusions from dated causes.

## Frontier check

Precedents: R2 L26; R3 L08; R4 L34, L44, N27; R5 L08, L34, L26; R6 L35; R7 L08, L34, L26; R8 L08, L34. L08 and L34
are this build's own platform runs (architectures 6 and 7).
Shallow path checks: the own-count weighting reconciles to the balancer hour by hour and its bootstrap is tight; only
each kept span's root against the edge services' kept counts (the export against the balancer at the root's grain)
refutes it. The export read as December has no missing hour inside it; its first span's time against the calendar,
and the span metrics' rows before it, refute it. A same-hour or load fill of the early hours back-tests well on the
held hours; the span metrics' counts for the early hours themselves refute or confirm it. The whole-window cause
passes a plot of excess by service; the order of the rises refutes it.
Assumption made false: "the retained spans represent the requests of each service and hour" (the run on file wrote
it): false because retention is decided at the trace's root, tested by the roots' kept counts; "the export covers
December": false by 274 hours, tested by its first span; "a bucket's spans are spread evenly inside it" (the tool's
default): false in a tail, tested where the export holds the same spans.
Forcing: the lines are the budgets. The golden family (26 splits of the bucket, three weight bases) files the five
every time, journey-search between 0.78 and 0.85 against 1.0 and the over-budget services no nearer their line than
partner-gateway's 0.29; the naive bridges and both bounds file the five (journey-search 0.76 to 1.04, the upper bound
on its line); the shortcuts file seven other lists; the split shares moved 20 per cent either way keep the five
(effort.json `forcing`).
Noun swap: `skeleton.py check task6`: no severity 1 or 2; the nearest client task weights a sample by its design and
carries neither the second grain nor dated causes.
Closed strategies: the call turns on three lessons. `design_weights` sits next to the card "Rows are occurrences, not
the people you care about" (link records to the person, weight by one over multiplicity): here the unit is the request
and nothing is listed twice; the inclusion probability is set by another unit (the trace's root) and recorded
nowhere, and it has to be carried into a record with no root (the callers' mix from the client spans). The early
hours sit next to the completeness card (a gross-up by a recording share) and the card for a source calibrated on
checked cases: the remedy is neither a share nor a factor, it is a second record at another grain assigned to the
part of the estimand the first cannot see, weighted by a design it does not record and split at a threshold it does
not carry; the calibration card's fix (a factor from the overlap) is the pooled split, one member of the family, and
moves no verdict. The dated causes are on no card. Supporting closed lessons: the clustered interval (R6; a binomial
interval leaves the list standing).
Decisive steps: J1's answer is the first service to start and payments' SLI (partner-gateway; 0.2), asked for by
"starting with the one whose SLI counts the most requests over its threshold" and "every service's SLI", evidence in
the span export's parent ids and the balancer's RequestCount. J2's answer is the owner of each December incident's
root cause (INC-1611 fares, INC-1619 notifications, INC-1579 partner-gateway), asked for by "the service that owned
the root cause of each customer-facing incident in December", evidence in the spans' parent and child timing against
the balancer's load. J3's answer is places' and booking's December SLI (1.4 and 0.3), asked for by "every service's
SLI", evidence in the span metrics' rows before 12 December 10:00. Independence: without J1 places and seat-map;
without J2 partner-gateway, places, journey-search and seat-map; without J3 the five and journey-search; without J1
and J2 places, journey-search and seat-map; without J1 and J3 places, fares, journey-search and seat-map; without J2
and J3 partner-gateway, places, journey-search and seat-map.
Run routes: generous (every correction a shipped file checks at full strength: hourly own-count reweighting that
reconciles to the balancer, the early hours from the span metrics with the split calibrated on the overlap, causes by
the largest excess): places, journey-search and seat-map (the lattice's J1 and J2 lost). Calibrated (the split fitted
on the overlap as one pooled factor): the golden's list when J1 and J2 are made, so the split is a banded figure and
no stump. Hedge (the trace-root weighting or the early hours reported as a sensitivity, own counts and the export
central): the reflex route's list. Cut-off (the early hours handled by dropping them, an incident by dropping its
whole window for every named service): six, or journey-search over.
Validation handles: the span metrics against the export on the held hours score the bucket's split (banded, moves no
verdict) and nothing else; no file scores a weighting (the balancer's counts reconcile to own-count weights by
construction and hold no latency) and no file records a December cause (the reviews are open).
Forward window: none: the call reads a closed month under PR-SLO-3 3.1; the estimand is still not the record's own
mean, because the record is a sample kept at another unit's rate over part of the month.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | December in Lisbon time | UTC or local | the same: Lisbon is UTC in December | PR-SLO-3 3.1 |
| SF2 | over the threshold | strictly greater, or at least | strictly greater | PR-SLO-3 2.1 ("exceeded"); no span sits on a threshold, and a boundary's own count is "at or under" in both records |
| SF3 | a re-sent span id | once or twice | once | same call; the span metrics count each span once and agree with the de-duplicated export |
| SF4 | the balancer's probes | requests or not | not requests | PR-SLO-3 2.2; the export carries none |
| SF5 | a retried call | one request or two | two | PR-SLO-3 2.2 ("any call a caller sent") |
| SF6 | a request that ended in an error | counted or not | counted, the span metrics' error and non-error rows summed | PR-SLO-3 2.4 |
| SF7 | which window a request belongs to | its start or its end | its start | PR-SLO-3 2.4 |
| SF8 | the weighting base | the balancer's count, or the weighted kept count | either | same call |
| SF9 | the root's hour or the span's own hour | either | either | same call |
| SF10 | spans of traces begun before the export (their root dropped) | weighted on their own hour, or dropped | either | same call |
| SF11 | when a named service's window starts | the declaration, or the timeline's add time | the add time | PR-SLO-3 3.2; the prompt ("counting it from when the incident tool added it") |
| SF12 | when an incident ends | the tool's resolve time, or the status page's last operational change | the status page | PR-SLO-3 3.2 and 5.2 |
| SF13 | a December incident with no status post | left out or not | nothing left out | PR-SLO-3 5.2 (customer-facing means posted) |
| SF14 | the onset's lead window | two to four hours before the declaration | every lead gives the same causes | same call |
| SF15 | the shares' base | all ten SLIs' counted over-threshold requests | that | the prompt ("all our services' SLIs count") |
| SF16 | the interval's method | linearised or a trace bootstrap | either, each end within 0.03 | same call |
| SF19 | an onset's clock time | the changepoint's minute, an "about" time, or none | none in the answer blocks: they grade the owner | the verifier's detector dates onsets earlier with the same owner and order |
| SF20 | December's hours before the export's first span | left out (the export as December), or counted | counted, from the span metrics | PR-SLO-3 2.2 ("whether or not the tracing store kept a span for it") and 3.1; the span metrics' rows from 1 December |
| SF21 | how a threshold's bucket is split in those hours | one pooled share, two to thirty load bands, a logit in load, the hour of day; straight-line or log-linear interpolation; the bucket's bounds | five load bands | every split: same call, figures inside the stated ranges; interpolation and the bounds: same call, and for the figures ruled out by the held hours, where interpolation rebuilds 1.6 to 3.0 times the spans' own count |
| SF22 | where the export begins | the first span's hour | 12 December 10:00, a whole hour | the export's first span |
| SF23 | how an onset is dated | the golden's sustained changepoint, ten-minute medians, rolling medians | the sustained changepoint at a rise of 2.2 times | every detector calibrated on placebo windows names the same owners or abstains |
| SF24 | a fill that reads no span metrics | a flat share, a match on the hour or weekday, load bands | none: the hours are recorded | the span metrics' counts: partner-gateway 2.3 measured against 2.9 flat; load fills of eight bands or more land inside the stated ranges |
| SF26 | an internal operation's weight in the early hours | the callers' keep weights averaged over that hour's client spans, the operation's main caller, or the held hours' caller mix | the hour's client spans | same call |
| SF27 | the span metrics against the export where both hold an hour | the same spans or not | the same: identical counts by series and boundary | the two files |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| each service's threshold and budget | section 4's table | PR-SLO-3_service_level_objectives_2026.docx, section 4 (read by the golden) |
| the histogram's boundaries | 5 to 10,000 ms | tracing_span_metrics_2026-12.csv, its own header (read by the golden) |
| the hour the export begins | 274 | trace_spans_2026-12.parquet, its earliest server span (measured; spread none: the store drops whole hours) |
| the sampler's hourly keep share | the root's RequestCount over the roots kept | lb_target_group_requests_2026-H2.csv against the export's roots and, before it, the root series of tracing_span_metrics_2026-12.csv (measured per edge service and hour) |
| a bucket's split | by five bands of hourly load | measured on the export's held, incident-free spans; the split family's spread is each bridged SLI's stated range (0.03 to 0.07) |
| the load curve of own handling time | a quadratic in log hourly load per span name | fitted on the export's incident-free hours; spread: every rival detector on its own curve names the same owners |
| the onset rule | a rise of 2.2 times held half an hour and twenty spans | calibrated on placebo windows of the export (3 of 54 fire; at a doubling 4 of 54); spread: the same seven owners at every setting tried |

Variant battery: 33 variants the record supports (26 splits of the threshold bucket, thirteen forms weighted and
unweighted; three weight bases; four naive bridges) and four onset detectors file the same call, the five, and the 29
of them that are estimates (not bounds or interpolation) the same order and one-decimal SLIs. Sixteen fills that read
no span metrics were run beside them: load fills of four bands or more, an isotonic share and a curved logit file
the five; a flat share, the hour of day, the day type and two or three load bands file six, and the span metrics'
counts refuse them (partner-gateway 2.9 against 2.3 measured).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every request each service handled in December, kept or not (the hours before the export included), incident time left out per 3.2 | filed 2.2, 3.1, 3.2 (SF20) |
| 2 | Unit of account | the request (a server span when kept) | filed 2.1 and 2.3 |
| 3 | Attribution window | the time a request began | filed 2.4 (SF7) |
| 4 | As-of dating | the span export and the span metrics pulled on 12 January 2027; reviews open then | one pull, C1 (SF22) |
| 5 | Version basis | one export of each record, no revisions | C1 |
| 6 | Denominator | the requests a service handled less those left out | filed 2.2 and 3.2; SF8 corridor |
| 7 | Weighting | each span at its trace root's hourly keep share; each early series at its callers' | the sample's design; rivals same (SF8 to SF10, SF26) |
| 8 | Window length | December, 31 days | filed 3.1 |
| 9 | Boundary inclusivity | strictly over the threshold | filed 2.1 (SF2) |
| 10 | Rounding path | SLIs printed to one decimal with their ranges; every verdict holds rounded or not | the answer blocks; checks |
| 11 | Tie-break | none needed: the order's closest neighbours, seat-map and notifications, differ by 8 per cent in over-threshold requests and keep their places under every split and weight base | checks M3 |
| 12 | Maturity and censoring | the month is closed; December's reviews open, so causes are dated from the data; the early hours are counted from the span metrics | C1; filed 3.3; SF20 and SF21 |
| 13 | Order of operations | dedupe, link roots, weight, leave out, count the early hours, sum | C1 |
| 14 | Row order | export order | C1 |
| 15 | Duplicate resolution | a re-sent span once | SF3 |
| 16 | Identity normalisation | tracing names and target groups through the catalogue | the catalogue's crosswalk |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | nanoseconds to milliseconds; per cents | the files' own columns |
| 19 | Code and status semantics | 5xx, 404 and retries count as requests | filed 2.2 and 2.4 (SF5, SF6) |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | section 4's table for every service; 3.2 for every December customer-facing incident | filed |
| 22 | Forward window contents | none: the call reads a closed month | C1 |

## Literal reader

PR-SLO-3 2.1 to 2.4, 3.1 to 3.4 and 5.2 executed word for word give the golden's population, windows and verdict rule:
2.2's "whether or not the tracing store kept a span for it" with 3.1's December puts the hours before the export's
first span inside every SLI; 3.3 read literally puts each December incident on the service whose own handling failed,
and the data date that failure (no shipped sentence names a December cause or the store's retention). The prompt's
"counting it from when the incident tool added it" executes to the timeline's add times; "all our services' SLIs
count" executes to the shares' base. The prompt states no rounding: the answer blocks carry each figure's precision
and range.

## Prompt contract

A voice rewrite may not drop or change: the question (which internal services ran over their 2026 latency error
budget); the engineers' order (the service whose SLI counts the most requests over its threshold first: the first
judgment's own answer); in a short report each one's share of the over-threshold requests all the SLIs count, a 90 per
cent confidence interval on each one's SLI, the requests the services over budget served beyond their budgets, every
service's SLI in per cent beside its budget (the first and third judgments' own answers) and a chart, and the service
that owned the root cause of each customer-facing incident in December (the second judgment's own answer); a CSV with
each service's SLI, budget, verdict and incident minutes in each half of 2026 counted from when the tool added it. It
must never add a rounding instruction, a method (weights, traces, sampling, onsets, load, self time, histograms,
buckets), a warning, an attached file's name, a role, or a count the data hold.

## Build brief

World: Rotalinha as in `generator/world.py` and `common.py`; the store's span metrics are written by
`pack.write_span_metrics` from the same kept spans as the export, for every December hour.
Frozen: every dial in `common.py` (thresholds, targets, spreads, incidents, the sampler's 60, the store's 274th hour,
the histogram's boundaries) and every estimator in `analysis.py`.
Files: the fifteen of the approved cut and `tracing_span_metrics_2026-12.csv` (hour, service, span name, kind and
status; the spans ingested, the sum of their durations and the cumulative count at each boundary; no row for an empty
hour). It must not carry a column, a note or a name that says what it is for.
Never filed: that the export is short or why; that the span metrics are a sample or how to weight them; any word on
splitting a bucket; any December cause.
Goldens: `reliability_review_2026.docx` and `service_sli_2026.csv` from `figures.json`, the routes table in the
review.
Free: nothing in the analysis; texture only.

## Leak sweep rulings

- `capacity_review_2026-Q4.md`: Platform Infrastructure's own record (pods, CPU, memory, autoscaling); a distractor that
  describes no data and dates no December incident. Harmless.
- PR-SLO-3's figures that match golden figures are its own budgets (0.5, 1.0, 2.0) and a section number (2.3): filed
  inputs, not answers. Harmless.
- PR-SLO-3 carries the call's service names because its threshold table lists every service. Harmless.
- PR-SLO-3 3.1 to 3.4 and 5.2 fix the SLI's window, population and the incident exclusion, and 3.3 defines owning a
  root cause; they file the WHAT (the review's own standard), and no sentence says how to find the owner or that the
  spans are a sample to be weighted. Harmless, as designed.
- The span metrics' column names (`calls_total`, `latency_bucket_le_...`) are the metrics generator's own; they say
  what a column holds and nothing about the review. Harmless.
- The stump-vocabulary sweep's two lines (PR-SLO-3 and the capacity review share service names and "balancer" and
  "record" with the stump paragraph): service names from the standard's own table and the infrastructure review's own
  rows; neither names a move. Harmless.
- Leak reader on the repaired cut (2026-11-25, Sonnet at medium, a fresh copy of the prompt and the pack): no file
  ranks the services, none exists only to help, no figure or name reads as the answer, and no one thing makes the
  work routine; the sentences it quotes as fixing a computation are PR-SLO-3 2.1 to 2.4, 3.1 to 3.4, 5.2 and 5.4,
  the filed WHAT, each executing to the golden's population and windows. It read 5.2's minutes as running from the
  declaration; the prompt's "counting it from when the incident tool added it" settles that (SF11). Its two realism
  notes were checked and are not defects: the timeline's "event" row is the header, and the incident ids step
  unevenly (3 to 17).

## Pre-ship check

- Hidden factor record against the cut data: the edge sampler's hourly trace count shows for every edge service in
  every hour of both records; the export's first span is at 12 December 10:00 for every service and the span metrics
  hold every service in every December hour; counting the early hours moves eight of ten one-decimal SLIs, the
  deciding one among them; the bucket's split moves five services and none across its budget; the onset dating runs
  on every service each December incident named.
- Effort test against `effort.py` on the final cut: quick 11.0, careful but hurried 24.8, thorough 100; the largest
  hint rescues 1 of 8; a run that loses any one judgment keeps 37; six distinct wrong lists over ten shortcut routes.
- Rivals (checks SF21, SF24, SF26, SF27, R7): 26 splits of the threshold's bucket and three weight bases give the
  five, the order and every bridged SLI at one one-decimal value; interpolation and both bounds give the five (the
  upper bound puts journey-search at 1.04 unrounded, a bound and not an estimate); flat, hour and coarse load fills
  file six and miss partner-gateway's measured figure by 0.6; the same-weekday-and-hour fill puts journey-search at
  1.04; the bootstrap agrees with the linearised interval within 0.03. The independent verifier reproduces every
  figure on its own code path.
- The golden against the world: the store's own unshipped early spans give the same list (checks RES5), and a
  five-times sample of the same world puts every true SLI inside the golden's interval.
- Places' share of the over-threshold requests is 29.50, on its whole-per-cent line: the blocks print 29 and accept a
  point either way.
- Card: the fingerprint guard's check on the updated card has no BLOCK; its WARNs (the forum, the written document,
  the question form, design_weights next to a closed card and taught twice, the coverage lesson on two live builds,
  the decision form on four) are answered in Draw, Frontier check and Template check.
- freeze.py: determinism mode FAIL (120 frozen items moved) and rubric mode FAIL (27), expected and not cleared: a
  result was redesigned after a determinism return, so no mode's contract matches (pipeline.json `freeze`).
- Leak reader (2026-11-25): clean on the repaired cut, rulings in Leak sweep rulings. Determinism judge, pass 6
  (determinism mode, the Holistic Audit v4's Step 0 and Parts A and B): running at this commit.
- Gates on the final cut: `gates.py task6` 9 gates, 0 FAIL, 4 WARN (precut: no `generator/core.py`, a near chain
  with task7, the re-sent batch as routine texture, R2 upstream of four results; voice: the written document;
  leak.py REVIEW, ruled; heart: three WARNs); generator checks all passed, verify PASS, both builds byte-identical.

## Tried and rejected

- The seed's own stump, residential density against daytime presence, rejected at the draw on 2026-10-18: with the estimand filed as the people present, choosing presence over residents is reading the estimand (data semantics); left unfiled, the call is not determinate.
- Network ride times against straight-line catchments (urban network analysis), rejected at the draw: a filed twenty-minute ride makes the street network the literal method, so the decisive step would be rule application.
- The plug-in bias of the weighted density from noisy survey counts per tract, rejected at the draw: the same insight as task253 (sampling noise counted as signal).
- Attendance conditioned on commute distance as a continuous covariate, rejected at the draw: the functional form opens forks on every graded figure; the county type of residence carries the same structure with nothing to choose.
- A mobile-device presence panel, rejected at the draw: a column holding the deciding quantity scaled, which R1 forbids and which reads the call off.
- Six distinct winners on six rungs, tried in the prototype on 2026-10-18: consecutive corrections move the cores too little to clear 1.15x margins at every rung; the ladder keeps three rungs with their own winners (every job present, the share by industry group, the share by industry group and county type) and the work-from-home reflex as a hazard landing on rung 0's metro.
- The draw's prototype shares (other services 0.80, 0.45, 0.20 against a survey mix of 0.45, 0.30, 0.25 in every industry), set aside at stage 2 on 2026-10-18: a quarter of every industry's workers living outside their workplace's metro is not the national pattern; with the survey's mix by industry (other services 0.48, 0.30, 0.22) and the realistic shares, two office cores cannot both clear 1.15, so Corrisford became a port and logistics core whose drivers and remote sales staff, living mostly outside the metro, are seldom on the premises.
- The draw's registration slot, set aside at the end of stage 2 on 2026-10-18: the draw-time `guard.py check` ran before the pull that brought in task165 (composition_mix, operations_director, registered at 14:10) and task167 v2 (population, E, method_or_model_selection, 06:59), so the card filed at 16:11 carries ban.strategy, ban.role and test.same_driver BLOCKs against them; three conditioning-transfer drivers in one batch is the template the bans exist for, and the composition stump is this seed's own pitfall, so the design is kept and the card re-registered once the batch has moved past them.
- Architecture 1 (the survey's share of weekdays on the premises carried onto each commuting flow within industry group and the type of county the worker lives in), spent at stage 4 on 2026-10-18: the isolated reader, working the cut pack cold at medium effort, carried the share by industry group and HOMEREL onto every flow as a matter of course and committed Tessavon at 28,805 against Corrisford's 21,709 (`score_reader.py` exit 1, the call 5 of 5, every core density); the decisive rung was readable through the schema, because the survey carries the residence relation as a column the codebook defines against the workplace's metropolitan area, which types every flow through the delineation file, and an analyst carrying a survey rate onto counts carries it on every classifier the two sources share, so the stratum the design called decisive is the careful analyst's reflex. The judge found the call forced and Gate H passing, and two ask forks (a workplace outside any metropolitan area is HOMEREL 4 in the codebook where the golden typed those flows 3; Ask B's partner-shop rule unfiled). In this world a stratification the survey's own columns invite cannot carry the stump; the re-root draws a decisive step no classifier the sources share can reach.
- The seed DA18's world itself, set aside at the re-root on 2026-10-18: every lever the weekday-presence measure offers is a rate carried within strata the survey and the counts share (residence relation, commute distance, shift times, firm size), which the careful analyst stratifies on by reflex, or a choice the board paper already files (residents, primary jobs, latest releases, the core's tracts).
- Length-biased sampling (a census-day stock of stays weighted by inverse length, a stop's random-arrival wait), set aside at the re-root draw: task264 in this lane already weights members sampled in proportion to their events, and a wait read with the inspection paradox is the transit field's standard excess-wait formula, a reflex for a strong solver.
- Measurement-error deconvolution of a distribution's tail, set aside at the re-root draw: task246 deconvolves measurers' error and task253 in this lane shrinks noisy unit averages.
- Values below varying detection limits, detection-corrected counts, dual-list capture and capacity-censored demand, set aside at the re-root draw: task189, task242 and task462, task196 and task448, task168 carry them.
- A return-wave nowcast for leavers whose window is open (the seed DA19's natural stump) and a nowcast conditioned on whether a leaver's post is held, set aside at the re-root draw: task157 carries the calendar-gated return wave, and the held-post nowcast is a composition shift (`composition_mix`), banned against task165 in the window and spent three times in this lane.
- The stage-2 contraction model (each cell's density proportional to its habitat quality to a power solved each year), set aside at stage 3 on 2026-10-18: a large power pulls the deep band's own cells apart, so the band does not hold together and the survey's plain mean sat within noise of the stratified mean (Halmorie Deep 39 to 47 per cent against Brettach Bank's 48 in the structural runs); replaced by band multipliers, the basin read by depth band, with Halmorie Deep enlarged to 80 cells so its deep band is a tenth of the area, which puts the plain mean 14 points under the stratified mean before any noise.
- Torn and weather-missed survey stations placed anywhere, set aside at stage 3 on 2026-10-18: on Halmorie Deep or Brettach Bank a balanced-panel or imputation reading moved a graded fall across its rounding edge in most seeds; the torn stations are on Vallaskie Hole (rough edges to the hole) and the missed one on Cullardy Patch, and the call, both falls and the gap are asserted unchanged under either reading.
- Seeds 1 to 200 searched on cut packs for the ladder's margins, every graded figure 0.12 or more from its rounding edge, the gap the same from unrounded and rounded falls, the convergent readings printing alike and every ask figure missed by the cracker and the over-cleaners: seeds 22, 40, 67, 69, 94 and 184 passed; 69 kept, the widest clearance (0.31 points) with every rung's margin 1.18 or more.
- Architecture 2 (the members' catch rates against the autumn survey's fixed stations, each depth band weighted by its share of the ground's stock area), spent at stage 4 on 2026-10-18: the isolated reader, cold at medium effort, went to the survey first and weighted the bands by area as a matter of course, reading plan 4.2's "weight of haddock on its stock area" with the manual's equal stations per band, and committed Halmorie Deep at 63 per cent against Brettach Bank's 52 with every fall (`score_reader.py` exit 1); it never weighed the logbooks. The judge found the call forced and Gates G and H passing. A survey whose design document describes its strata and allocation, under an estimand filed as a total over an area, makes the design-based estimator the careful analyst's default rather than a stump; the preferential-sampling rung below it is never reached by a reader who reads the plan first.
- Architecture 3's first draft (a motor mutual's 2027 telematics pilot region by January to September claims frequency, the claims not yet notified completed claim by claim on their own notification channel's development, pooled or regional development over-completing the region that moved to the app), dropped before registration on 2026-10-18: it is task181 v2's per-route delay completion, which a solver landed once the estimand was filed, with task451's handler-speed change on top; a channel column makes the per-channel development the careful analyst's reflex.
- Re-root screens on 2026-10-18 before this draw, each set aside with its record: values below detection limits (task189, task190, task183, task248, task246), Pareto interpolation within an income band (task264's own rejection: no decision rests on it), a concentration-discharge rating curve's retransformation (task135 v1 and task452 v1: the textbook construction was the default), anchor equating of two test forms (task450, task464), demand censored at capacity (task168, task147), dual-list capture (task248, task253), informative dropout in a growth curve (task257: multiple imputation lands without the insight), the dissimilarity index's small-unit bias and tempo-adjusted fertility (each estimand names its method), beta-binomial reach extrapolation (two collinear forms fit four insertions alike) and classification consistency at a cut score (classical and IRT estimators split the figures).
- The first informative-censoring prototype (the retirement hospital's patients diagnosed later, 2026-10-18): with a worse class mix at diagnosis its true survival sat so far below the urban hospital's that Kaplan-Meier found it too; its difference now lies in age (death rates 1.10 to 1.18 times and worsening 1.25 to 1.4 times the others') on a mix like theirs, and the cardiology group's departure ends follow-up for over half of Wrenhaven's patients, so the worst-case and complete-case routes fall on Wrenhaven, not Gullhaven.
- The stage-3 world with Gullhaven's moves high in every class (a north intercept of -5.2 to -5.5, a death multiplier of 1.22 to 1.25), set aside at stage 3 on 2026-10-18: a third or more of Gullhaven's patients moved north within two years, more than a retirement coast's return of the frail carries; the moves now concentrate on class IV visits (a quarter of them end in a move) with the death multiplier at 1.16, so 22 per cent move, 96 per cent of them in class III or IV.
- Seeds searched under the kept world on cut packs (2 to 81, 302 to 347, 502 to 547, 2026-10-18): every rung's pick and margin, every form of the decisive estimator printing the same whole percent for every hospital, the golden 0.1 or more from its edges and every ask figure missed by the cracker; 28 and 515 passed, 28 kept (515's truth separated Gullhaven from Fennick by 0.7 points only). Seeds 2 to 123 of the earlier world, searched alongside, were dropped with that world.
- Ask B's re-enrolments under the new record number as its primary device, set aside at stage 4 on 2026-10-19: every solver maps the record numbers through the crosswalk to link the Florida deaths, and with every number current the re-enrolments show as one patient enrolled twice; the round-1 reader left all 143 out and hit all ten figures. They stay as a hazard.
- The overwritten diagnosis dates at the 2025 year end (a November 2025 module update), set aside the same day: they took December 2025 diagnoses out of a count by the date shown while the re-enrolments put patients in, and on the registry as it stands the two cancelled on one of Fennick's figures; at the 2024 year end both move the count the same way.
- Brenmoor's first mix at diagnosis (34 per cent in class III or IV), set aside at stage 4: the default path's gap, Fennick to Brenmoor at 2.26, printed 2 like the golden's Gullhaven to Fennick at 2.08, so a Kaplan-Meier response stated the graded gap's number.
- The relocation recorded on the date of the visit where it was reported, set aside at stage 4 on 2026-10-19 (the round-2 judge's SEND_BACK, margin_or_boundary_fragility): an analyst who takes the class from the visits before the loss date drops that visit and carries a third of Gullhaven's movers from the milder class of the visit before, which put the landmark and fixed-class estimators at 66.9 to 67.3 against the golden's 64.9 and the gap at 2, 1 or 0. The registry now records a relocation when it processes that visit's note, one to four days later (manual 3.3), so the last visit precedes the loss date under every convention.
- A move allowed only after a quarter in the same class, tried the same day to close that convention instead: it made the move depend on the class history, so weights by the class at the visit no longer matched the moves and the projection fell 0.4 to 1.1 points below the weighting in every seed searched.
- The re-consent deadline of 1 April 2024, moved to 1 January 2025 the same day: 942 withdrawals with up to twenty months left carried Wrenhaven's figure from 71 to 73 across the estimators; with a year at most left it holds at 72 under every one, and leaving the withdrawn out still names Wrenhaven.
- The round-1 and round-2 world (Gullhaven's class-specific death rate 1.16 times the others', class IV improving 8 per cent a quarter, moves at 2.2 per cent of class III visits and 24 per cent of class IV), rejected after stage 4 round 2: the judge's class-adjusted estimators put Gullhaven between 64.9 and 67.3 per cent; pooled outcome models imported the other hospitals' death rate and the fixed-last-class and landmark models misread the movers' improvement, so the gap read 2, 1 or 0 by method.
- A seed search in that world with the relocation dated after the reporting visit (450 seeds), rejected: two seeds kept every by-hospital form in one bin, none with the pooled forms agreeing, and their leads were a point; luck in the seed was not a forced answer.
- Wrenhaven's re-consent on 1 January 2025 with three in four withdrawing, rejected in fix pass 2: its 2023 patients carried up to a year past the withdrawal spread the estimators 0.5 points on Wrenhaven; the deadline moved to 1 May 2025 with nine in ten withdrawing, the spread 0.3, the dropped and dead-counted readings still on Wrenhaven.
- A later deadline with Wrenhaven's mix unchanged (1 March or 1 May 2025), or 1 June with it sicker, rejected in fix pass 2: too few withdrawals for the dropped and the dead-counted readings to land on Wrenhaven rather than Gullhaven, and the complete-case route then lands Gullhaven within a point of the golden's figure.
- The discrete projection counting a death only within 91 days of a visit, corrected in fix pass 2: a visit kept late or missed dropped about one death in twelve, so the projection ran 0.2 to 0.5 points high on Gullhaven.
- Ask A asked as "the NT-proBNP tests its laboratory reported", replaced in fix pass 3: read literally every released row is a reported test, so counting a corrected specimen once rested on a supersession rule no file states (stage 4 round 3's judge); the unit is now the specimen, filed in the prompt, and no correction crosses the referral level.
- Portal round 1 (2026-10-28): both responses missed the call (rubric average 12.5); both determinism judges failed it as answer_contradicts_files, reading the charter's 3.2 ("Every patient ... counts, including patients the registry no longer follows") as the deaths on file over every patient, a lost patient counted alive (R0, Fennick). Not a redesign: closing the reading leaves the default path (Kaplan-Meier, Fennick) where it was. Repaired at the WHAT only: 3.2 now puts every patient in the share and says the registry does not learn of the deaths of the patients who left follow-up; SF13 asserted; the write-up's steps say why the deaths on file cannot stand for survival and why the class at the move carries a lost patient's chance of dying. No estimator filed.
- Determinism repair, round 1 of the portal (2026-10-28), sent back: with 3.2 reworded the re-judge (pass 5) accepted the crude reading as closed, then returned NOT_DETERMINISTIC, SEND_BACK. Gate C: plain Kaplan-Meier, every move as ordinary censoring, is a standard reading every filed rule allows and names Fennick (61.16 against Gullhaven 62.35), while carrying the lost from their class is filed nowhere; Gate G: the mechanic classed single_conceptual_flip, a standard statistic rejected as misleading. Two corrections of one graded quantity (determinism-check section 3): filing the class-carried estimator makes the decisive step rule application, filing Kaplan-Meier makes Fennick the answer, so the stump lives in the fork and no closure keeps it. Redesign of the decisive step at stage 2 (/build task6 from 2): keep the registry world if a split off the censoring treatment can be found, else re-root. Carry forward: 3.2's wording that closes the crude reading (every patient in the share as they were at two years; the lack of a death on the registry's files does not show a lost patient alive; a first wording, "whose deaths the registry does not learn of", was still read as alive by default), the deck's embedded-workbook stamps pinned, the Linux-only rebuild, and block 1's Wrenhaven count, 347, which did not reproduce (931 every CNR event, 336 those inside the two-year window).
- Architecture 4's first card labels, Gate G `forecasting` and strategy `composition_mix`, withdrawn on 2026-10-28 before any data was cut: the vocabulary defines forecasting as a forecast the correctly read past does not pin, and this design's closed years pin the development; composition_mix and the executive forum then met task270 v11's bans. Redrawn to method_or_model_selection, forecast_method_backtest and committee_or_panel, each the honest key.
- A notifying-channel column on the claims extract (Policyholder, solicitor, claims-management company and the rest as one field), rejected at stage 2 on 2026-10-28: with the Standard's back-test filed, every grouping the extract's own columns offer is an enumerable model class behind a shipped test, which the library records as an answer key (task38). The extract keeps the claims system's coarse notified-by field, and the firm type lives on the representatives table.
- Region-level development as the default, with no filed selection criterion, rejected at the draw: task127 v3 and this slot's architecture 3 died at the judge for leaving the method open. The Standard files the back-test in general terms and puts regional estimates on the whole book's factors (3.2), so each region's own development is against the text as well as failing 2022.
- A Severn own-damage rate at its first value and a Pennine wave of 0.55 per 100 car-years, measured on the prototype on 2026-10-28: the route split itself named Mersey and Severn (Pennine 8.03 against 8.25). The wave became 0.85 per 100 car-years and Severn's own-damage rate 7 per cent lower; seed 5 is the first of six where every route-based development prints the same five figures and the back-test separates at 1.1 against 6.8 per cent.
- Ask B (private-car claims notified on 2026 accidents by region, injury against the rest, the online notification journey's abandoned first records as its device), retired at stage 4 on 2026-10-28: the determinism judge's first pass found the call and Ask A uniquely forced and Ask B open, because no shipped file says the abandoned record is the phoned claim and the Standard's 2.1 ("every claim notified counts once, including claims closed without payment") reads literally for counting it. The device cannot be both determinate and silent: identity filed or carried on the row, the careful solver executes 2.1 and the cracker keeps the ask; left unfiled, it is a fork. The twins were taken out of the world (2026 rows only, no figure of the call moved) and the ask layer became the cars on cover by all three covers, the reconstruction the judge confirmed.
- Architecture 4 (a motor insurer's 2027 telematics pilot regions, the claims not yet notified developed by notifying route, the route built by joining each claim's representative to the representatives table), spent 2026-10-31 on the learning loop's paper screen: the route sits one join away (the notified-by field and the representatives table) and development by notification channel is the reserving field's own refinement, so the decisive rung was a reflex; the slot moves to marketing-consumer-research (segmentation-market-structure), a new world, dataset, generator and prompt shell.
- Marketing draws screened on paper before this one, 2026-10-31: excess duplication judged over shoppers whose stores stock both brands (task281's note: filing the co-availability population is rule application, leaving it unfiled forks the call); a receipt-scanning panel whose submissions rise in a brand's bonus weeks (the correction needs a submission model, so the estimator family is open); a sub-panel's cross-media duplication applied to the full panel (one consistency check of the sub-panel's TV reach against the full panel's lands it); an exposure crediting quirk in the as-run log (reading what a record means, data semantics); mystery-shopper audits inflated by detection (the calibration against the CCTV census is the natural data-fusion reflex and reaches the golden).
- The bank-card reference carried on the till lines themselves (a card alias beside the Rewards card on every row), set aside at stage 2 on 2026-10-31: a self-join on a column of the main file is the one line of code the survivor anatomy's Link test refuses, so the card reference lives only in Faircourt's settlement file, reached by a match on terminal, time and amount.
- A card acceptance cost by store and quarter as the settlement file's own ask, set aside at stage 2 on 2026-10-31: the cost belongs to another owner (finance) and the organisation already has it on Faircourt's monthly statements (H18); the settlement file's second use is the counter's card payments instead.
- The Roastery's own loose beans at the counter, set aside the same day: a home buying them would open a fork on what buying the Roastery means; the counter sells guest roasters only.
- A link standing on any single shared payment, measured on the prototype on 2026-10-31: with one in three couples' links resting on one or two shared payments, a reading that needs two or three moved Oro Rosso's share by six points and named Nordhavn at three; a home's shared card is now a habit (used three times or more by each card it links, the weaker uses falling back to the member's own card), so one, two and three shared payments build the same homes.
- Counter labels matched only to card payments, set aside the same day: the counter's card takings would tie to the sold labels (an oracle for both devices); cash customers pay at the main tills and the counter terminal also takes accessories, so no total ties.
- Seeds 1 to 81 and 101 to 266 screened on the in-memory world on 2026-10-31 for every rung's winner and margin (1.15, the decisive 1.2), the runner-up a point clear of third, every share off its rounding edge (the call and runner-up by 0.15), the gap rounding alike from unrounded and rounded shares, link thresholds identical, online accounts alone never naming the call, both asks' figures off their edges and the cracker missing every ask figure: seeds 263 and 276 passed; 263 kept (its one-line adjustment stop keeps 4 of 20 against 276's 11).
- The counter's card terminal as the only way to pay, and a scale clock reset in April, set aside in the stage 3 build on 2026-10-31: with no cash route the counter's takings tied to the sold labels, and a two-week April reset moved only three cells; cash labels now go to the main tills, the reset runs 22 June to 14 July across the second and third quarters, and the funding rates are odd cents so no quarter sits on a half euro.
- Multibuy deals whose cheapest pair cost less than the deal price, found in the stage 3 build: a pair of Cafetto Original 200g at 14.98 against a two-for-15.00 deal produced negative savings; every deal now lists packs of one price.
- The counter's matching left to windows the pack never stated (stage 4 judge, FIX_NOW): 122 card sales read two ways at
  one total and 114 cash lines had two same-priced labels; the board now files the 25 minutes, the same day and the
  void at closing, and the generator re-weighs any label that allows a second reading under any window near them.
- Architecture 5 (the rival whose buying homes least often also bought the Roastery, homes assembled from the Rewards cards and online accounts that share a bank-card token in Faircourt's settlement file), spent at its first portal round on 2026-11-07: both responses named Oro Rosso, each building homes through the settlement file's card reference (one response lists its "household-linkage" assumptions). The prompt and the brief file the unit as the home, which determinism requires, and once the home is filed the shared payment card is the only record that joins two cards, so the linkage ran as a work order: filing the estimand announced the rung, and the construction is the join that cleaning the data already asks for (Layer 1 carrying the stump). No closure keeps it, since leaving the unit unfiled forks the call between cards and homes. The slot re-roots to architecture 6 in another world, dataset, generator and prompt shell, with a decisive step that no filed unit or join announces.
- Architecture 6's first candidate, set aside at the draw on 2026-11-07 before registration: a Lisbon ticketing marketplace's internal service latency SLIs read from a trace store kept under head-based sampling set per entry route, each downstream span inheriting its trace's entry rate (checkout in full, search at one per cent), so the services checkout calls look slow until each span is weighted by the inverse of its trace's entry rate. The setting and driver hit no slot note, but task452 v2 (shipped) already teaches the insight: weight each sampled record by the inclusion probability of the stratum it was drawn in, not the grouping it is analysed by. One sentence covers both, so the draw would read as a clone. The guard also showed the signature crowded: gap population with method_or_model_selection is spent on G14 (ten builds), G9 (five), G6 (nine) and E (the slot's own architecture 1), and G12 is banned against task190.
- Architecture 6's second candidate, set aside at the draw on 2026-11-07: a ride-hailing platform's 2027 background-check vendor, which moves a driver sign-up inside the activation target only where the check cleared last, the other requirements (documents, vehicle inspection, training) running alongside it. The slot screen found it spent: task127 v2 (the portal landed it) credits an intervention only with the replaced step's excess over a concurrent step, and task472 v2 credits saved work only where it moves a release into an earlier window.
- Architecture 6 first drawn with a per-service hourly sampler (2026-11-07, registered 21:54:53Z, pack built and golden
  reproduced on seed 2718): it cleared the ladder on 51 of 60 seeds (golden ratio 1.31, wrong-route margin 0.14) and was
  superseded before stage 2, because once a service's kept spans read flat at the sampler's target each hour, the hourly
  reweighting is one join from the load balancer's counts and both top responses would take it; it is rung 3 here.
- SLIs to two decimals on the edge-sampler world (2026-11-07): the standing estimators (Horvitz-Thompson on the balancer's
  count, Hajek, hour-calibrated) spread 0.01 to 0.08 points on the internal services, so almost no seed held all three on one
  two-decimal figure; SLIs are reported to one decimal, the precision 744 hours of about 24 kept traces an edge service carry
  (the golden and the world's truth differ by 0.05 to 0.1).
- accounts' sign-in texts sent through notifications (2026-11-07): 4 per cent of sign-ins, about one kept text an hour, each
  weighted at about 150 requests, moved notifications' estimate 0.3 points between seeds and opened the corridor to 0.08;
  removed from the call graph.
- Partner-gateway's seat inventory read set to a target slow share (2026-11-07): 0.25 per cent at 1,000 ms forced a 340 ms
  median, which alone put 19 per cent of seat maps over their 500 ms line; set to a fixed 85 ms read.
- Ask A, each service's releases and rollbacks in 2026, dropped at the rubric repair on 2026-11-08: both platform runs
  rebuilt production's history from the pipeline log and the rollout history and filed every figure the rubric tested
  (12 points, run 1 off the call included); the reconstruction is part of a frontier run's battery and no figure reads
  the SLI, so it could not be re-sited downstream of the deep step.
- Ask B, each service's cloud cost by half, dropped at the rubric repair on 2026-11-08: both runs followed the
  replacement links, converted US dollars at each invoice's rate and netted credits, filing every tested figure (19
  points each); no cost figure reads the SLI.
- Ask C as every service's customer-facing incident minutes by half, replaced on 2026-11-08 by the minutes in which an
  incident named at least one of the services that ran over: run 1, off the call, read 5.2's naming clock and kept all
  17 points while run 2, on the call, read the export's final lists from the declaration and lost them; per service the
  cells of services both paths name are free to a careful run off the call, while the union over the call's services
  moves with the call (1,545 and 907 against the default path's 1,518 and 755) and keeps the naming clock as the ask's
  own judgment (1,571 and 1,067 on the final lists).
- Critical components 2 and 3 (journey-search, places, seat-map and notifications at 1.3, 1.5, 1.5 and 1.6; fares,
  tickets, accounts, booking and payments at 0.6, 0.6, 0.7, 0.4 and 0.3), replaced on 2026-11-08: each is an edge or
  single-caller service the default path reproduces exactly, so run 1 kept their 14 points (rubric rows 3, 4 and 20) off
  the call; replaced by the trace mix behind partner-gateway's weights and the start-order and programme figures.
- Every service's share of the over-threshold requests as a column of service_sli_2026.csv, set aside during the
  2026-11-08 repair: booking, payments and tickets round to 0 and notifications to 1 per cent on every rung, so four of
  ten cells are free to the default path (a shallow keep of 21 per cent and a paper pair of 61.8); the shares sit in the
  review for the services the call names, where the default path keeps one of five.
- The incident ask's naming clock as its own judgment, closed on 2026-11-08: the determinism judge read PR-SLO-3 5.2
  ("named it at the time") as not saying which record defines naming, so the final-list reading (1,571 and 1,067) is a
  licensed alternative, and a loss there is a misread clause rather than an analytical one; the prompt now pins it
  (SF16), with the minute unit (SF17) and the joint share's base (SF18).
- **Architecture 6, returned at final review (2026-11-09, version 17, every platform check passed).** The breach list turned on one thing: each kept span weighted by its root edge service's hourly keep share, which moved only partner-gateway (1.4 to 2.9 per cent against 2.0, four services over to five). The reviewer called it a shallow hidden factor (built into the data so it decides one service; a single weight once noticed) and asked for the sampling to touch several services partially and for the breach list to rest on several connected pieces (weighting, periods, incident attribution). Re-rooted to a results chain in the same world, on the reviewer's own direction.
- **Architecture 7 at stage 2 (2026-11-09): five measured redesigns before the chain held.** An incident at the Cyber Week peak made journey-search and seat-map cross their budgets on attribution alone (an edge flip, the review's own example of a planted factor): the faults moved off the campaign peaks and journey-search's threshold to 1,500 ms. Notifications first flipped on the weighting alone (0.65 against 1.32): its slow operation moved to the thinly kept caller. "Most slow requests in the window" then attributed every flip correctly, so the root weighting alone rescued half the results: the 26 December incident gained the queueing of accounts' sign-ins behind the SMS calls, which out-slows the true cause on every simple measure but not on its onset. Seeds: 12 of 39 held the list, 3 of 20 every margin; seed 2711 chosen. Health probes were dropped from the export (as roots of internal services they gave absurd weights; the edge sampler never sees them), and the SMS incident's pre-symptom evidence was widened (the fault from 17:00, accounts' queueing from 18:30, more sign-ins sending a code) after the independent verifier dated it to accounts on five spans.
- **INC-1619 as the only incident where a blocked caller outran the fault, rejected at stage 4 on 2026-11-09:** the
  hurried attribution went wrong in that one incident, which alone decided notifications, the returned shape (one
  constructed factor deciding one service) in the attribution leg; rebuilt with the same pattern in INC-1611 (deciding
  fares) and INC-1579 (deciding nothing), every slowdown ramped from uneven times, and three faults strengthened so the
  over-budget intervals clear their budgets by 0.08 or more.
- **The shipped architecture 7 against the strong run, measured on 2026-11-09:** a run dated every cause right and lost
  only on the weighting; with the careful pass calibrated to it, the weighting sentence rescued three or four of six
  results (level 3). Levelled up with the store's retention (the dropped first eleven days of December, filled at their
  load), which the run's own habits do not catch; the cut is backed up in ~/Documents.
- **Early-December campaigns at saturation (3 and 10 December), rejected while levelling up:** they drove
  partner-gateway past anything the held days show, so every fill extrapolated and the forms disagreed by up to 0.27
  (journey-search 0.63 to 0.90); the first fortnight is now ordinary trading, as the calendar has it.
- **A New Year sale from 11:00, rejected:** its midday hours saturated seat-map and bent its load curve, losing
  INC-1570's onset; the sale runs on the evening only.
- **24 kept traces an hour, rejected:** the held hours' over-threshold counts were too sparse for the fill forms to
  agree at one decimal (places 1.36 to 1.47); 60 an hour.
- **The getaway push on the evening of 17 December, moved to the 16th:** it ran under INC-1594 and its load bent
  notifications' curve, so a rolling-median dating flagged a false rise; the verifier now dates by its own changepoint.
- **The onset rule at 1.4 times on any split, rejected:** it fired on 37 per cent of placebo windows, a last few noisy
  spans passing for a rise; now one sustained changepoint (half an hour and twenty spans each side) at a doubling, 6 per
  cent, and the four faults at 1.6 to 1.8 times that sat under the quiet days' floor are 2.6 to 2.8 times.
- **The verifier's rolling median as the check of the owners, rejected:** it was rival evidence (no window got both
  deciding incidents right uncalibrated); the rival detectors now sit in checks R7, calibrated on placebo windows.
- **Architecture 7 as shipped, returned on 2026-11-22 (review sheet of November 22, reward 45.0, Stumped passed, Determinism (main) failed):** journey-search's verdict turned on how the 274 hours before the export were filled. Reproduced on the shipped pack on 2026-11-25: 1.33, 1.31, 1.17, 1.13 and 0.97 with two to six load bands, 0.89 with seven to thirty, an isotonic share and both logits, 1.18 matching weekday and hour, 1.36 flat, 1.32 on the export's hours alone. The fork-is-the-result test: a flat fill is the export's own share, so closing the fork toward any fill the reviewer named puts the hurried figure in the band; the result is redesigned, not pinned.
- **The reviewer's second fix taken as it stands (journey-search moved clear so every load fill agrees), rejected on 2026-11-25:** with no record of the early hours every fill is an extrapolation, the honest family runs from the flat share to fine load bands (partner-gateway 2.3 to 3.1, places 1.4 to 1.7), every SLI's accepted range would have to hold it, and the hours before the export would grade nothing. It removes a judgment and loosens every figure.
- **The reviewer's first fix taken as it stands (the early spans shipped), rejected the same day:** nothing is left to estimate and the remedy is a union of two exports.
- **A load balancer latency statistic for the early hours, a slow-trace triage pull and a kept-trace index, each screened on paper and rejected the same day:** an all-request latency figure per service and hour scores any weighting against a known answer and hands the trace roots' weights over; a slow-only pull needs each early hour's kept-root count, which only the sampler's rule gives, and its remedy is the weights again; an index of root durations measures the edge services with nothing to build.
- **The tracing store's span metrics on the OpenTelemetry default boundaries, kept (2026-11-25):** the store's own hourly duration histogram of the spans it ingested outlives the spans, so the early hours are recorded, at a coarser grain: no trace, no root, and five of ten thresholds inside a bucket. The verdicts are forced by counts; the figures need the bucket split and the callers' weights.
- **Booking at 3,000 ms, payments at 2,000 ms and tickets at 1,500 ms under the span metrics, rejected:** each threshold sat in a bucket holding 1 to 12 per cent of the early hours' spans, so straight-line interpolation inside the bucket moved booking, payments and tickets across their budgets. Tickets at 1,000 ms and payments and booking both at 2,500 ms were infeasible (a ticket request's partner call alone exceeds 1,000 ms too often; a booking cannot be faster than the payment it waits on). Kept: booking 2,500, payments 1,000, tickets 2,500, each a boundary.
- **Partner-gateway's availability latency spread at 0.40, 0.37, 0.46, 0.48, 0.49 and 0.50, each measured and rejected:** at 0.40 journey-search sat at 0.89 with interpolation at 0.99 and the bucket's upper bound at 1.04; a tighter spread moved it up (1.45 on the export's hours at 0.37); at 0.49 partner-gateway's exact figure sat on a rounding edge (2.252). Kept: 0.52 with the availability target at 2.26 (journey-search 0.81 across December, 1.14 on the export's hours; partner-gateway 2.29), accounts' own target 1.15 and notifications' verification target 1.02 so neither crosses its line at a bucket bound.
- **The generator's corelib proof (a `generator/core.py` ending on `corelib.run`), not built for this repair:** the card was registered on 2026-11-09, before the core rule, and the same quantities (the lattice of the three judgments, the split family, the naive bridges, the load fills, the forcing block) are computed on the cut pack by `analysis.py` and written to `effort.json`. corelib's two-sided row would also refuse the third judgment as built: every bridge of the early hours, the bounds included, files the same list, which is what the review asked for.
- **freeze.py on this repair:** no mode matches a result redesigned after a determinism return (graded figures move by design: three thresholds, journey-search's level, every SLI through the measured early hours); both modes' outputs are recorded in pipeline.json rather than a snapshot retaken to pass.
- **The onset rule at a doubling on the repaired cut, recalibrated (2026-11-25):** with partner-gateway's availability spread widened it fired on 4 of 54 placebo windows (journey-search's own handling at the evening peaks of 18, 22 and 23 December), over the one-in-fourteen line it is calibrated to; at a rise of 2.2 times (level 1.9) it fires on 3 of 54. The seven owners were the same at every setting tried (2.0 to 2.2, level 1.75 to 1.9), so no window and no SLI moved.
- **A binomial interval as the interval result's hurried figure for every over-budget service, narrowed to the internal three:** with the early hours measured, seat-map's interval is a binomial one to 0.002 (every kept span of an edge service is its own trace at one weight an hour) and places' misses by 0.026; partner-gateway, fares and notifications miss by 0.047, 0.032 and 0.035. The interval is a supporting figure, never a judgment the list turns on.
- **The start order's tenth-of-a-count margin, restated at a twentieth:** raising notifications clear of its line at the bucket's lower bound brought it to within 8 per cent of seat-map in over-threshold requests; the order holds under all 26 splits and three weight bases, and the answer blocks name the margin.
- **The world's own unshipped early spans against the split (checks RES5):** the same list and the five boundary services identical; places (1.35) and accounts (1.19) land just under their split ranges, inside their 90 per cent intervals, from the binomial noise of which bucket spans crossed the threshold. The stated ranges are what the record supports, the intervals carry the rest.
- **A five-times sample of the same world (300 kept traces an hour, scratch run of 2026-11-25) as the truth check:** journey-search 0.71, fares 1.32, places 1.39, seat-map 1.89, booking 0.33, payments 0.22, tickets 0.67, accounts 1.18, partner-gateway 2.26, notifications 1.34 with the standard's exclusions under the world's own faults: the golden five, each of these inside the golden's 90 per cent interval where one is computed.

