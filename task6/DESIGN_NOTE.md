# task6: Rotalinha's internal services over their 2026 latency error budget (architecture 7, levelled up)

## Draw

The design of architecture 6 (the single deep step it was returned for) is in git history at commit bd3bbed.

- **Card.** `.claude/skills/fingerprint/cards/task6.json`, architecture v7, registered 2026-11-09T16:23:04Z with
  `--force` on one axis: `ban.pairing` against task2 (general-statistics-data-science with Descriptive & Distribution
  Analysis). The platform assigned this returned task its domain and analysis type (task 4b456953, version 17, task
  type match passed), so the re-root keeps the pairing; the reason is in the card's notes. Axes redrawn against the
  window task2, task12, task13: stump_strategy population_selection to causal_design (task12 holds the old label, and
  v7's flips rest on the incident attribution against load together with the weighting, not on the population
  alone), context_artifact operations_log to monitoring_export (the balancer's metrics export and the trace store's
  span export are what the review reads), org_family software_or_platform to retailer_or_ecommerce (Rotalinha sells
  bus and ferry tickets online). WARNs answered: overuse.forum (the engineering leadership group that approved
  PR-SLO-3 staffs the programme; no other forum holds the decision), repeat.deliverables csv+docx against task13 (a
  per-service table and a review document is the genre of an SLO review).
- **Why the same world.** The final review asked for this task to be fixed, not replaced: "make the sampling affect
  several services in different, partial ways, each with a checkable SLI; let the breach list depend on several
  connected pieces (weighting, periods, incident attribution), not one weight; trace-level weighting can stay as one
  step among several." The world keeps its people, files and sampler; the call graph, the December incidents and the
  standard's incident clause are what change.
- **Levelled up (2026-11-09).** The shipped architecture 7 met a strong run that dated every cause right and lost
  only on the weighting, so on the run-calibrated pass one sentence rescued three or four of six results (level 3).
  The level-up adds a second judgment the runs miss, from the same world's process: the tracing store keeps 31 days,
  the review pulled December's spans on 12 January, and the store had already dropped everything before 12 December
  10:00, so a third of December's requests have no spans and still count. The backup of the shipped cut is in
  ~/Documents/task6_arch7_backup_2026-11-09.zip.
- **Pairing.** general-statistics-data-science / missing-data-censoring-measurement-error / descriptive-distribution.
Analysis type: Descriptive & Distribution Analysis (where each service's December latency share really sits, once the
sample's design weights, the December hours the sample no longer covers and the incident time charged elsewhere are
handled).
Answer shape: a flagged set with the evidence: the services over budget with each SLI, its interval and the December
incidents' root causes behind it, in the order their engineers start.
Weight: a hard-to-measure quantity: each service's share of slow requests from a whole-trace sample whose inclusion
probability is recorded nowhere and which no longer covers the month's first eleven days, with incident time charged to
the service that owned each incident's root cause. The
last builds leaned on attribution (task13), robustness (task2) and forecasting (task12).
- **Decision.** Which internal services ran over their 2026 latency error budget; each gets a reliability engineer
  for January to June 2027, the one whose SLI counts the most requests over its threshold first. Retrospective by
  design: the SLO year closed on 31 December 2026 and the programme starts in January.
- **Data-native sentence.** The trace store keeps whole traces at the edge, a fixed number an hour per edge service,
  so every internal service's kept spans carry the keep shares of the several edge services that call it, in a mix
  that differs from the traffic's; December's incidents were faults in one service's own handling that reached the
  services calling it, at the evening peaks when every service is already slower with load, and the responders named
  the services in the order they suspected them; and the store keeps 31 days, so by the January pull it had dropped
  December's quieter first eleven days, whose requests the balancer still counts.
- **People.** Teresa Nogueira (Head of Platform Reliability), Bruno Marques (FinOps), Ivo Pereira (SRE): the
  personas drawn for architecture 5's world and kept with it.

## Deep reasoning

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), serving Descriptive &
Distribution Analysis: a population share estimated from a sample whose inclusion probability is set by another unit
and recorded nowhere, which covers only part of the population's period, with part of the population left out by a
filed rule whose membership has to be established.
Domain test: the field's own estimators for a share from a stratified cluster sample with unequal, unrecorded inclusion
probabilities (Horvitz-Thompson or Hajek, each trace weighted by its root edge service's hourly keep share), the
imputation of a period the sample does not cover from an auxiliary variable it does (each service's hourly load from
the balancer, its over-threshold share by load band on the held hours), the design-based variance of the combined
ratio, and a changepoint on load-adjusted residuals to date which service's own handling degraded first.
Swap: "which hospital wards ran over their waiting-time budget" breaks at once: a ward has no trace root whose keep
share sets every other ward's inclusion, no call tree that makes one ward slow because another is, and no store that
drops a month's first weeks while the census still counts them.
Where the weight sits: the hard-to-measure quantity, every service's December SLI: the kept spans are a cluster sample
drawn at the edge, so four internal services carry their callers' keep shares (fares, partner-gateway and notifications
up, payments down); a third of December's requests have no spans at all and have to be carried in at the share their
hour's load gives; and the incident time PR-SLO-3 3.2 leaves out depends on a root cause no review has recorded yet.
The work is long because each piece has its own evidence, not because one piece is clever.
Layer 1: re-sent span rows from the exporter's retries (the same span id twice, neutral, asserted); traces begun in the
hour before the export whose root the store had dropped (any handling, same one-decimal SLIs); the balancer's target
groups renamed on 1 July (the catalogue's crosswalk); the status page in Lisbon local time against the incident tool's
UTC; the incident export's final service lists against the timeline's add times; 404s, 5xx and a retried
partner-gateway call counting as requests. None moves a graded result except the incident minutes, which grade the
timeline reconciliation itself.
Not one thing: three judgments each move the list, and each alone leaves it wrong. The trace roots' weights over the
export's hours alone give six (journey-search over at 1.3); the dropped hours filled on each service's own hourly count
give places and seat-map; the weights and the fill with each incident on the service furthest over its curve give
journey-search, places, seat-map and partner-gateway. The intervals, the minutes and the shares each need their own work.
One-fact test: on the careful pass calibrated to the run record (own hourly counts, every cause dated right, the
export's hours alone), "each kept span counts at its trace root's hourly keep share" rescues none of six results, "the
store had dropped December's first eleven days, which still count at their load" rescues none, and the dating sentence
rescues nothing the run did not already earn (effort.json, measured).
Not semantics: every field, unit and clause read correctly (the re-sent rows, the windows, the halves, the zones) still
leaves the own-hour weighting at fares 1.2, partner-gateway 1.4 and notifications 0.7 and journey-search at 1.3 on the
export's hours.
Not rule application: PR-SLO-3 files what an SLI is, that a request counts whether or not the store kept a span, which
incident time leaves it and what owning a root cause means; no filed rule weights a span, says the export is short,
fills the hours it lacks, dates a degradation or builds an interval. Executing every filed rule with the textbook
own-hour reweighting over the export's hours files journey-search, fares, places and seat-map.
Estimand: PR-SLO-3 3.1 (December in Lisbon time), 2.1 to 2.4 (every request a service handled, kept or not, its server
span's duration, by the time it started, errors counting), 3.2 (incident time from when the tool added the service to
when the status page showed every component operational, left out unless the service owned the root cause), 3.3 (a
service owns it when the failure was in its own handling, systems outside the catalogue included; a service that slowed
only because a catalogue service it called slowed does not), 3.4 (a breach is the SLI over the budget), 5.2 and 5.4
(the minutes, the halves).
No decoy: no memo, draft or stakeholder figure; the capacity review and the app reviews are context the golden never
reads; the closed reviews record causes only for January to November, and nothing names December's; no shipped
sentence mentions the store's retention.
No replay: no shipped figure is re-derived; no stated number is wrong.
Pinned: every rival estimator on every SLI lands on the same one-decimal value (checks R7: Horvitz-Thompson, the span's
own hour, the orphans dropped); every way of filling the dropped hours at their load that the held hours support (ten
or twenty load bands, an isotonic share, a quadratic logit, the called services' loads beside the service's own, and
fitting windows two or four hours clear of incidents) gives the same one-decimal SLIs; a share linear in log load is
rejected by the held hours (curvature, chi-square on one degree of freedom) wherever it would move a cell; the matches
that ignore load (the same weekday and hour, the hour of day, weekday or weekend by hour, a flat share) and a load model
with hour-of-day terms are ruled out out of sample: fitted from 18 December and predicting the export's own 12 to 17
December, the load bands' mean log error is 0.28 against 0.41 to 2.9, and summed over services they predict 0.81 of
the over-threshold requests seen against 1.30 to 1.96; the trace bootstrap with the fill refitted lands within 0.04 of
the linearised interval. The onset rule (one sustained changepoint, a doubling) fires on 6 per cent of placebo windows
(each incident's window moved by whole days onto the export's quiet stretches), and every rival detector calibrated
the same way (ten-minute medians, half-hour and hour rolling medians) names the same seven owners or sees nothing;
the onset over a two- and a four-hour lead does too. The verifier's changepoint is the golden's rule on its own code
path, a check of the code, not rival evidence.
Run forecast: a strong run loses R3 to R6 by method shortcut (each service's own spans reweighted on its own hourly
count) and by a narrow look at broad data (December read from the export's twenty days: journey-search 1.3, over), as
the run on file did on the first; a weaker run also stops at the first story on R2 (the 14, 21 and 26 December
incidents on seat-map, journey-search and accounts); R4 falls to a method shortcut (a binomial interval, and no
allowance for the filled hours); R1 to a narrow look (the export's final service lists read from each declaration).
Strategy label: WORKS IN FORM (variance and inclusion that the sample's design sets, and missingness by design, from
`sulfur-strategies.md`'s clean comparison and heterogeneity rows read as results) for the weighting and the fill, and
the client's own investigation shape for the attribution (dating onsets to separate cause from symptom), each one
result among six.
Depth level: 5 on the client's scale, measured on the run-calibrated pass. Three judgments that each move the list and
each need estimation (the trace roots' weights, the dropped hours carried in at their load, the causes dated by own
handling against load), a fourth with its own figure (the design-based interval with the fill's uncertainty), and five
distinct wrong lists from five shortcuts; the largest single hint rescues none of six results.
Lesson: an estimate from a sample drawn somewhere else, over a period it no longer covers, must carry that sample's
design and its coverage throughout (weights, the missing period filled from what still measures it, units of the
interval), and an incident's cause is the earliest degradation once load is taken out, not the service the responders
named or the one that suffered most; no build on file pairs a design-weighted share with a coverage gap and dated causes.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each service's customer-facing incident minutes in each half of 2026 | Assembly and reconciliation | PR-SLO-3 5.2 and 5.4; the timeline's add times; the status page's last operational change | exact | narrow look at broad data: the export's final service lists read from each declaration, or the tool's resolve time as the end | - | Ask 1 |
| R2 | the service that owned the root cause of each December customer-facing incident | Investigation loops | PR-SLO-3 3.3; own handling time against a load curve on the export's incident-free hours; the earliest held rise | exact | stopped at the first story: the service named first, or the one furthest over its curve across the whole incident (14, 21 and 26 December on seat-map, journey-search and accounts) | R1 | Component 1 |
| R3 | every service's December latency SLI | Missingness and measurement | PR-SLO-3 2.2 (kept or not), 3.1 and 3.2; each span at its trace root's hourly keep share; the dropped hours at their load band's held share; the windows R2 leaves out | exact at one decimal (every rival fill and weight) | method shortcut (own hourly counts) and a narrow look at broad data (the export's hours read as December) | R1, R2 | Ask 2 |
| R4 | a 90 per cent confidence interval on each over-budget service's SLI | Uncertainty | the trace store's design: strata of root service and hour, whole traces as units, each also moving the fill's band shares | the linearised and bootstrapped ends, 0.02 either side | method shortcut: a binomial interval on the kept spans, no allowance for the clusters, the weights or the filled hours | R3 | Component 4 |
| R5 | the services over budget | Synthesis | PR-SLO-3 3.4 on R3 | exact | unfinished chain: the SLIs from the export's hours (journey-search over) or on own counts (partner-gateway and notifications within) | R3 | Recommendation |
| R6 | the start order, each one's share of the over-threshold requests the SLIs count, the share together and the requests beyond budget | Decomposition and attribution | the SLIs' weighted and filled numerators and counted requests | exact at the asked rounding | method shortcut: shares of the kept over-threshold spans on the own-hour weights over the export's hours | R3, R5 | Ask 3 |

Carry-forward: R1 stands alone (the incident records only). R2 needs only R1's windows. R4, R5 and R6 fall with R3, and
R3 needs the weighting, the fill and R2 together: no single analytical result is the only one behind them
(`precut.py`'s count), and the largest hint rescues no result (effort.json).

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| whole traces kept at the edge, a near-fixed 60 an hour per edge service | constructed (the world's sampler) | no: it moves all four internal services (fares, partner-gateway and notifications up, payments down) and every interval | a targeted query: each kept span's root against the balancer's hourly counts | a reweight by the root's keep share, routine once seen | keep, one result among six |
| the store's 31 days: the export begins at 12 December 10:00, a third of December's requests without spans | constructed (the store's retention and the review's pull date) | no: every service loses the same hours, and the early weeks' lighter load moves each SLI by its own load sensitivity (journey-search 1.3 to 0.9, fares, places, seat-map, partner-gateway and notifications all move a tenth or more) | one look at the export's first span; the size of the gap by the balancer's counts | modelling: each service's over-threshold share by load band on the held, incident-free hours, carried to the dropped hours, with its uncertainty in the interval | keep |
| December faults in one service's own handling (2.6 to 3.9 times its handling time), reaching the services that call it | constructed (seven incidents in six services) | no: nine services named, faults in six, one incident on a single service | modelling: own handling time against a load curve, a changepoint per span name | modelling | keep |
| callers' workers waiting on a slow call late in an incident, in three incidents further over their curves than the fault | constructed (five of seven incidents; ramped, uneven onsets) | no: journey-search, seat-map, booking and accounts; the larger-than-the-fault form in INC-1579 (decides no verdict), INC-1611 and INC-1619 (fares and notifications) | modelling: onset order, not size | modelling | keep |
| evening, holiday and campaign load raising every service's handling time | constructed (the world's queueing curve, the Christmas weeks, two campaign evenings) | no: every service, every day | modelling: the load curve itself | modelling | keep |
| the exporter re-sending a batch | constructed (one batch in three hundred) | no | a query: a repeated span id | routine | keep, texture (moves nothing, checks R2) |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 incident minutes by half | Missed | Right | Right |
| R2 root cause of each December incident | Missed | Right | Right |
| R3 every service's December SLI | Missed | Missed | Right |
| R4 intervals on the over-budget SLIs | Missed | Missed | Right |
| R5 the services over budget | Missed | Partly | Right |
| R6 start order, shares, together, beyond | Missed | Missed | Right |
| Roughly | 0 of 6 | 2.5 of 6 | 6 of 6 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (each pass's methods run end to end on the cut
pack by generator/analysis.py: quick unweighted with the first-named service at fault, the export's hours alone and the
export's lists from each declaration; careful calibrated to the run record, each service's own hourly count with every
cause dated right, the export's hours read as December and binomial intervals; thorough the golden).
Largest single hint: each kept span counts at its trace root's hourly keep share; rescues 0 of 6 results.
Pair estimate: 44.3
Routes (`effort.json` routes, the golden's other-readings table): unweighted, first named, export's hours: seat-map;
own counts, dated, export's hours (the run on file): journey-search, fares, places and seat-map; root weights, dated,
export's hours: those four with partner-gateway and notifications; own counts, dated, dropped hours filled: places and
seat-map; root weights, whole-window causes, filled: journey-search, places, seat-map and partner-gateway; only the
root weights with dated causes and the filled hours give the five.
AND: R3, R5 and R6 need the weighting, the fill and R2 together; each sentence alone leaves the list wrong in a
different way, so none rescues a result on the run-calibrated pass (judge passes 2 to 4 each found a fresh reader
overclaiming the weighting sentence on the earlier cut; on this one it moves the list and still leaves journey-search
over).

## Data provenance

Source: generated by task6/generator from a simulated platform (seed 2711): hourly traffic for six edge services, the
calls each request makes to four internal services, queueing latency under load, an edge sampler keeping about 60 whole
traces an hour per edge service, a tracing store that keeps 31 days, and December's incidents as faults in one
service's handling.
Behaves like the real thing: latencies are log-normal with a queueing curve in each service's hourly load, as service
latency is; the sampler is head-based and per trace at the edge, as OpenTelemetry's rate-limiting samplers are; the
store deletes whole hours past its retention, as block-based trace stores do, so a pull in January no longer holds
early December; callers inherit their callees' slowness and queue behind them late in an incident, as thread-pool
services do; responders name the paging service first and add the cause as they find it, as the closed reviews show.
Genuine patterns: (1) diurnal peaks per service and a weekend dip (2) December seasonality: a quiet first fortnight,
the Christmas weeks and two campaign evenings (16 and 28 December) (3) queueing under load, steepest for partner-gateway
(4) per-operation latency that differs by caller (5) incidents that start before they are declared and end after
mitigation (6) a retried partner-gateway 5xx.
Problems by process: the exporter re-sends a batch (repeated span ids); the store's retention leaves the export
starting at 12 December 10:00, with orphan spans of traces begun in the hour before; the balancer renamed its target
groups on 1 July; the status page writes Lisbon local time and the incident tool UTC; the tool's export carries each
incident's final service list while the timeline dates each addition; December's reviews were still open on the export
date.
Breadth: ten services, 744 December hours (470 of them in the export), 723,170 span rows across 174,121 traces, 44,160 hourly balancer
rows, 85 incidents with 581 timeline events and 41 status posts, so choosing what to read and at what grain is work.

## Template check

Chain signature: assembly-reconciliation, investigation-loops, missingness-measurement, uncertainty, synthesis,
decomposition-attribution
Question form: which, then how much and how sure
Nearest build: task13 (an outage record and a ranked list of feeders by modelled exposure); the nearest chain on file
dates no cause and weights no sample. The abstraction sentence a reviewer would write for task6 and task13 ("rates
read through a model of exposure") does not hold: here the weights come from a sample's design and the exclusions from
dated causes.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | December in Lisbon time | UTC or local | the same: Lisbon is UTC in December | PR-SLO-3 3.1 |
| SF2 | over the threshold | strictly greater, or at least | strictly greater | PR-SLO-3 2.1 ("exceeded"); no span sits on a threshold |
| SF3 | a re-sent span id | once or twice | once | same call (checks R2) |
| SF4 | the balancer's probes | requests or not | not requests | PR-SLO-3 2.2; the export carries none |
| SF5 | a retried call | one request or two | two | PR-SLO-3 2.2 ("any call a caller sent") |
| SF6 | a request that ended in an error | counted or not | counted | PR-SLO-3 2.4 |
| SF7 | which window a request belongs to | its start or its end | its start | PR-SLO-3 2.4 |
| SF8 | the weighting base | the balancer's count, or the weighted kept count | either | same call (checks R7) |
| SF9 | the root's hour or the span's own hour | either | either | same call (checks R7) |
| SF10 | spans of traces begun before the export (their root dropped) | weighted on their own hour, or dropped | either | same call (checks R7) |
| SF11 | when a named service's window starts | the declaration, or the timeline's add time | the add time | PR-SLO-3 3.2; the SLIs are the same either way (checks R2) |
| SF12 | when an incident ends | the tool's resolve time, or the status page's last operational change | the status page | PR-SLO-3 3.2 and 5.2 |
| SF13 | a December incident with no status post | left out or not | nothing left out | PR-SLO-3 5.2 (customer-facing means posted) |
| SF14 | the onset's lead window | two to four hours before the declaration | every lead gives the same causes | same call (checks R7) |
| SF15 | the shares' base | all ten SLIs' counted over-threshold requests | that | the prompt ("all our services' SLIs count") |
| SF16 | the interval's method | linearised or a trace bootstrap | either, within the band | same call (checks R7, the effort band) |
| SF20 | December's hours before the export's first span | left out (the export as December), or counted | counted, each service's requests at the over-threshold share its held, incident-free hours show at the same load | PR-SLO-3 2.2 ("whether or not the tracing store kept a span for it") and 3.1 (December); checks R3 and R5 |
| SF21 | how the dropped hours are filled | ten or twenty load bands, an isotonic share, a quadratic logit, the called services' loads beside the service's own, fitting windows two or four hours clear of incidents; or a match that ignores load, or load with the hour of day | ten load bands | the load forms: same call (checks R7); a share linear in log load: rejected by the held hours' curvature; the load-free matches and the hour-adjusted model: ruled out by the backtest on the export's own 12 to 17 December (checks R7) |
| SF23 | how an onset is dated | the golden's sustained changepoint, ten-minute medians, rolling medians, a CUSUM | the sustained changepoint at a doubling | every detector calibrated on placebo windows to one false alarm in fourteen names the same owners or abstains (checks R7); uncalibrated detectors fire on 15 to 98 per cent of placebo windows |
| SF22 | where the export begins | the first span's hour | 12 December 10:00, a whole hour | checks R4 |
| SF19 | an onset's clock time | the changepoint's minute, an "about" time, or none | none in the answer blocks: they grade the owner and the order of each pair of rises; the review's "about" times grade nothing | the verifier's rolling median dates every onset 15 to 55 minutes earlier with the same owner and order (verify.py; checks SF19 keeps the order at five minutes) |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every request each service handled in December, kept or not (the dropped hours included), incident time left out per 3.2 | filed 2.2, 3.1, 3.2 (SF20) |
| 2 | Unit of account | the request (a server span when kept) | filed 2.1 and 2.3 |
| 3 | Attribution window | the time a request began | filed 2.4 (SF7) |
| 4 | As-of dating | the span export pulled on 12 January 2027 (holding from 12 December 10:00); reviews open then | one export, C1 (SF22) |
| 5 | Version basis | one export, no revisions | C1 |
| 6 | Denominator | the requests a service handled less those left out | filed 2.2 and 3.2; SF8 corridor |
| 7 | Weighting | each span at its trace root's hourly keep share | the sample's design (R3); rivals same (SF8 to SF10) |
| 8 | Window length | December, 31 days | filed 3.1 |
| 9 | Boundary inclusivity | strictly over the threshold | filed 2.1 (SF2) |
| 10 | Rounding path | SLIs to one decimal and compared as rounded; intervals two decimals; shares whole; the rest once at the end | prompt; checks M1 |
| 11 | Tie-break | none needed: the order's neighbours differ by more than a tenth | checks M3 |
| 12 | Maturity and censoring | the month is closed; December's reviews open, so causes are dated from the data; the hours the store dropped are filled at their load | C1; filed 3.3; SF20 and SF21 |
| 13 | Order of operations | dedupe, link roots, weight, leave out, fill the dropped hours, sum | C1 |
| 14 | Row order | export order | C1 |
| 15 | Duplicate resolution | a re-sent span once | SF3 |
| 16 | Identity normalisation | tracing names and target groups through the catalogue | the catalogue's crosswalk |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | nanoseconds to milliseconds; per cents | the export's own columns |
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
count" executes to the shares' base.

## Prompt contract

A voice rewrite may not drop or change: the question (which internal services ran over their 2026 latency error
budget); the engineers' order (the service whose SLI counts the most requests over its threshold first); in a short
report each one's share of the over-threshold requests all the SLIs count, a 90 per cent confidence interval on each one's
SLI, every service's SLI beside its budget and a chart, the service that owned the root cause of each customer-facing
incident in December, and the requests beyond budget; a CSV with each service's SLI, budget, verdict and incident
minutes in each half of 2026 counted from when the tool added it; the rounding (SLIs and budgets one decimal, intervals
two, shares whole, minutes whole, requests to the nearest ten thousand). It must never add a method (weights, traces,
sampling, onsets, load, self time), a warning, an attached file's name, a role, or a count the data hold.

## Leak sweep rulings

- `capacity_review_2026-Q4.md`: Platform Infrastructure's own record (pods, CPU, memory, autoscaling); a distractor that
  describes no data and dates no December incident. Harmless.
- PR-SLO-3's figures that match golden figures are its own budgets (0.5, 1.0, 2.0) and a section number (2.2): filed
  inputs, not answers. Harmless.
- PR-SLO-3 carries the call's service names because its threshold table lists every service. Harmless.
- PR-SLO-3 names words that are also column names (Service, Tier, commit, component, cost, deployment): the standard's
  own vocabulary in its own sections, describing no file. Harmless.
- The as-of date is now in `metadata.json` (2027-01-06); the prompt's shell-quota warning is voice, for the author's
  rewrite.
- Architecture 7 reader (2026-11-09): PR-SLO-3 3.1 to 3.4 and 5.2 fix the SLI's window, population and the incident
  exclusion, and 3.3 defines owning a root cause; they file the WHAT (the review's own standard), and no sentence says
  how to find the owner or that the spans are a sample to be weighted. Harmless, as designed.
- The capacity review's forward note names partner-gateway's connection pools: a capacity plan after two December
  incidents it owned, beside journey-search's index move; no figure, no SLI, and a careful run that files
  partner-gateway within budget on its own hourly count is not moved by it. Harmless.
- The load balancer's hourly grid has no missing hour: a balancer's RequestCount is stored per minute and exported
  whole, and the quietest target group serves 93 requests in its quietest hour, so no hour is empty. Harmless.
- The incident titles read as templated (ten phrases, an "(N services)" suffix): fixed in the generator, each title now
  the commander's phrasing of the first-named service's symptom, drawn from the incident id; no graded figure moved.

## Pre-ship check

- Hidden factor record against the cut data: the edge sampler's hourly trace count shows for every edge service in
  every held hour, and the callers' mix moves every internal service's SLI; the export's first span is at 12 December
  10:00 for every service, and filling the dropped hours moves six or more one-decimal SLIs, the deciding one among
  them (checks R5); the onset dating runs on every service each December incident named.
- Effort test against `effort.py` on the final cut, the careful pass calibrated to the run on file: quick 7.0, careful
  but hurried 44.3, thorough 100; the largest hint rescues 0 of 6; five distinct wrong lists over five shortcuts.
- Rivals (checks R7): every weight base, every fill form the held hours support and both fitting windows give the same
  one-decimal SLIs; the linear-in-log-load fill is rejected by curvature; the bootstrap with the fill refitted agrees
  with the linearised interval within 0.04. The independent verifier reproduces every figure on its own code path.
- Leak reader (2026-11-09, on the levelled-up cut): no sentence hands over a step, no ranking, helping or answer file, no
  one thing; it read the export's gap as a tracing rollout that adds work. Its one realism note (the span export's
  Parquet footer named no writer) is fixed: the footer names the store's own Go writer.
- Judge pass 5 (2026-11-09, on the levelled-up cut before the onset rule was calibrated): DETERMINISTIC, every
  load-bearing figure reproduced, no competing answer, every spec gate passed; SEND_BACK on Gate H, estimating that a
  careful run earns the weighting on sight (the internal services never root a trace) and reading INC-1611 and
  INC-1619 as one flip applied twice. The first estimate runs against the run on file, which saw the trace structure
  (it dated causes by parent and child timing) and still weighted per service-hour; the careful column here is that run.
  The second is right that the two incidents share one judgment, which is R2's own; the list rests on R2 beside the
  weighting and the dropped days, each measured alone at no rescued result.
- Gates on the final cut: `guard.py heart` BLOCKs on ban.pairing against task2 v5, accepted by the author for this
  re-ship on 2026-11-09 (the returned platform task's own subdomain and analysis type).

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
