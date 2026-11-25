# task6 determinism check, pass 6 (Holistic Audit v4, determinism mode)

In-house replay of the platform's Holistic Audit v4, Step 0, Part A and Part B, 2026-11-25; prompt.txt 872f5a970163e53c0a800ca2255d7e64, target.zip e6a97cf82c049fe58c7a3c96fae6467e, submission.md 9d9c338ffcc0682b046943f4ec7482cc; no runs yet. Workspace /tmp/holistic-task6-determinism-j7tcl24j (scripts in work/).

**Verdict: DETERMINISTIC. Disposition: FIX_NOW** (changes to the answer blocks only: three ranges and four Step-by-Step sentences; nothing solvers see changes).

## Step 0

Golden present (all four fields carry computed values). The inputs belong to the task: every service, incident id, file and date the blocks name is in the pack.

## The audit's lines

**correctness:** correct. Every deciding figure reproduces from the shipped files. One interval end sits just outside its own tolerance, and four claims about alternatives in the Step-by-Step do not reproduce as written (see mismatches).

**figures_checked** (mine from code, then the author's):

| Figure | Mine | Author | Agree |
|---|---|---|---|
| Services over budget, in start order | partner-gateway, places, fares, seat-map, notifications | same | yes |
| Shares of all SLIs' over-threshold requests | 33.3 / 29.3 / 17.0 / 3.2 / 2.9 | 33 / 29 / 17 / 3 / 3 | yes |
| Excess over budgets, the five together | 195,751 | 200,000 (190k to 220k) | yes |
| SLIs: journey-search, fares, places, seat-map, booking | 0.795, 1.292, 1.388, 1.932, 0.326 | 0.8, 1.3, 1.4, 1.9, 0.3 | yes |
| SLIs: payments, tickets, accounts, partner-gateway, notifications | 0.210, 0.719, 1.210, 2.288, 1.300 | 0.2, 0.7, 1.2, 2.3, 1.3 | yes |
| 90% CI partner-gateway | 2.168 to 2.409 | 2.17 to 2.41 | yes |
| 90% CI places | 1.258 to 1.517 | 1.27 to 1.55 | **upper end is 0.033 out (tolerance 0.03)** |
| 90% CI fares / seat-map / notifications | 1.198-1.387 / 1.797-2.067 / 1.194-1.407 | 1.20-1.40 / 1.80-2.07 / 1.19-1.42 | yes |
| Root-cause owners INC-1570, 1579, 1588, 1594, 1611, 1619, 1627 | seat-map, partner-gw, partner-gw, payments, fares, notify, places | same | yes |
| CSV incident minutes, H1 and H2, all 20 cells | e.g. seat-map 690/216, notifications 99/680 | identical in every cell | yes |
| Critical components (partner-gateway first; payments 0.2; the three owners; places 1.4; booking 0.3) | as above | same | yes |
| Early hours: 274, 33% of edge requests | 274, 32.8% | 274, 33% | yes |
| seat-map against notifications in over-threshold requests | 1.079 | 8% more | yes |

How I derived them: kept each server span once (2,207 re-sent rows dropped). Weighted each span by its trace root's hourly keep share (root target-group RequestCount divided by roots kept that hour). For 1 to 12 Dec 09:00, used tracing_span_metrics' server series, weighted by the callers' client-series keep shares, and split each in-bucket threshold by the incident-free held spans' over-share in five load bands. Left out the named services' requests from when they were added until the status page showed operational, unless the service owned the cause. Dated each cause by a per-operation changepoint on own handling time (span duration less its child client spans) against a quadratic-in-log-load curve fitted on incident-free hours. Intervals by linearisation over strata of root service and hour, with traces as units, plus binomial terms for the early hours and the split. Incident minutes come from matching the status page posts (Europe/Lisbon) to the incidents, merging intervals per service and splitting at 30 Jun 23:00 UTC.

**mismatches** (Part A step 5: claims about alternatives must be true when computed):
1. Step 9 says "the bucket's two bounds" give the same list. They do not. Counting the whole bucket over threshold (the ceiling) puts journey-search at **1.039%**, so the list becomes six. The floor does give five.
2. Step 6 says straight-line interpolation "rebuilds 3.0 times ... places and 1.9 times ... journey-search". I get 3.22 and 2.03 on all the export's hours, and 3.34 and 2.86 on its incident-free hours. Neither reading gives 3.0 and 1.9.
3. Step 10's closing says "a fill that ... gives the early hours the export's own share puts partner-gateway at 2.9%". That fill gives **3.06%**. 2.9 comes out only from two load bands (2.93) or the same weekday and hour (2.88).
4. The leave-out of the dated causes alone says "fares 0.8%, journey-search 1.2%". I get **0.745 and 1.146**, which round to 0.7 and 1.1. The list matches.
5. Places interval: see the table above. The interval tolerance (each end within 0.03) is also tighter than the SLI ranges allow. Places at 1.44 under the pooled split, inside its 1.37 to 1.45 range, gives an interval of 1.31 to 1.57, whose lower end is 0.04 off. Fares at 1.33 gives 1.24 to 1.43.

**decision_reproduces:** yes. Same five, same order, same owners.

**determinism:** pinned. Every rival that moves the list or the order is refuted by a figure computed from the shipped files (evidence below). The rivals that are not refuted move graded figures only.

**unpinned_forks:** none that move the call. Two defensible rivals move a graded figure out of its range without moving the call:
- An interval-censored lognormal fitted to each early hour's histogram (the strongest standard rival) gives the same five, same order, excess 206,187. But it puts fares at **1.349** (range 1.27 to 1.34) and accounts at **1.340** (range 1.20 to 1.26). On the export's hours it overstates accounts' in-bucket over-threshold count by 46% (120 against 82), which refutes it for accounts. For fares it overstates by only 8% (244 against 226), which is not a refutation. Close both by widening the ranges.
- The interval method: the split choice moves each interval's ends by more than 0.03 (mismatch 5).

**giveaway:** none. incidents_2026.csv leaves root_cause_service empty for every December incident (review_status open). No file states an SLI, a budget comparison or the sampling.

## Evidence: the fork list run

Each row gives the list it files, whether a graded figure leaves its range, and the refutation where the list changes.

| # | Fork | List (start order) | Graded figure out? | Ruling |
|---|---|---|---|---|
| 1 | Root keep share (blocks) | pg, places, fares, seat-map, notif | no | |
| 2 | Each service's own hourly count | places, seat-map (pg 1.008, fares 0.888, notif 0.693) | yes | Refuted. pg's availability calls are 82% of its root-weighted requests but 26% of its spans. Weighting by roots reproduces pg's own RequestCount hour by hour (median ratio 1.004, range 0.95 to 1.06). |
| 3 | Denominator: balancer count instead of weighted kept count | same five | no | |
| 4 | Calibrated to RequestCount per service-hour | same five | no | |
| 5 | Root's hour or the span's own hour | same five (44 spans differ) | no | |
| 6 | Spans whose root is not in the export | none exist: 0 orphans, every one of 174,122 traces has a root | n/a | |
| 7 | Re-sent span ids kept | same five | no | |
| 8 | Early-hour split: pooled; bands 2, 3, 5, 10, 20, 30; logit in load; hour of day | same five, same order (js 0.78 to 0.85, places 1.38 to 1.44, fares 1.29 to 1.33, notif 1.29 to 1.30, accounts 1.20 to 1.22, excess 193k to 212k) | no | |
| 9 | Straight-line interpolation / log-linear | same five, but **places first** and notif ahead of seat-map (places 2.05 / 1.90) | yes | Refuted. On the export's hours they rebuild 3.2 times / 2.7 times places' over-threshold spans, and 2.0 times / 1.7 times journey-search's. |
| 10 | Bucket bounds: none over / all over | five / **six** (js 1.039) | yes | Refuted (the all-over bound rebuilds 2.95 times js's over-threshold spans on the export's hours). It also contradicts Step 9. |
| 11 | Lognormal histogram fit | same five | fares 1.349, accounts 1.340 | Band (see Fix) |
| 12 | Fills without span metrics: export hours alone; flat share; bands 2, 3; weekday-hour | **six** (js 1.136, 1.136, 1.104, 1.101, 1.047) | yes | Refuted. Even counting every early js span between 1,000 and 2,500 ms as over caps js's December SLI at 1.039. The metrics equal the export exactly where they overlap (10,388 series-hours, 447,526 spans, 0 mismatches). Leaving the early hours out entirely is barred by standard 3.1 (December) and 2.2. |
| 13 | Fills without span metrics: bands 5 to 30 | same five | yes | |
| 14 | Internal operation's early weight: own count / unweighted | same five (fares 1.205, notif 1.211, pg 2.175, pay 0.265, excess 164k) / six | yes | Refuted. On the export's hours the own-count rule rebuilds 0.43 times pg's and 2.17 times payments' root-weighted over-threshold requests; the callers rule rebuilds 1.00 times. |
| 15 | Cause detector grid, per operation on own time (bins 5/10/15 min, z 0.5/1/1.5, run 2/3/4, lead 1 h/3 h; 54 settings) | blocks' owners in 52 to 54 of 54 per incident | no | |
| 16 | Detector pooled per service | 1579 to seat-map: five (seat-map **2.13**). 1619 to accounts: **four** (notif 0.918) | yes | Refuted per operation. pg's seats endpoint rises at 12:10 to 12:20 (own median 269 ms against 94) before seat-map at 12:40 to 12:50 (437 against 120). notify's sms/verification rises from 17:00 (601 to 1,004 ms against 208) before accounts at 18:30 (361 against 54). |
| 17 | Furthest over the load curve across the incident (own time / total duration); first-added owns; nobody owns; clause ignored | pg, places, js, seat-map / places, fares, js, seat-map / places, js, seat-map / places, seat-map / six | yes | Refuted by standard 3.3 and the onsets in row 16 |
| 18 | Window: start at declaration; end at the tool's resolved time or mitigation | same five (tool resolved: js 0.758) | marginal | Pinned by standard 3.2 (added, status page) |
| 19 | SLI rounded to 0.1 before comparing / rounded to a whole per cent | same five / seat-map alone | no / yes | Whole per cent is unreasonable: the budgets are written to 0.1 |
| 20 | Incident minutes: status page read as UTC; count from declaration; end at the tool's resolved time | moves the CSV minutes | yes | Pinned. The file declares Europe/Lisbon, and read as UTC 19 of 41 posts come before their incident. The prompt says "from when the incident tool added it". Standard 5.2 ends at the status page. |

The strongest rival (house rule 2) is row 11, the lognormal histogram fit, and row 4, calibration. Neither moves the list or the order.

## Fix (where: solution only)

1. Supplementary 2b and 4b: fares SLI range **1.27 to 1.35**. Supplementary 2h: accounts **1.20 to 1.35**. These take the lognormal fit.
2. Supplementary 1: interval tolerance **each end within 0.06**. Re-centre places on the reproduction, **1.26 to 1.52** (the other four stand).
3. Step 9: replace "so do interpolation inside the bucket and the bucket's two bounds for the list" with this: interpolation and the floor give the same five but not the order or the figures; the ceiling (every span in the bucket counted over) puts journey-search at 1.04%, and on the export's hours it rebuilds 2.9 times journey-search's over-threshold spans.
4. Step 6: "3.2 times ... places and 2.0 times for journey-search" (on all the export's hours), or state the hour set that gives 3.0 and 1.9.
5. Step 10's closing: the no-metrics fill at the export's own share puts partner-gateway at 3.1% (not 2.9%). The leave-out of the dated causes alone gives fares 0.7% and journey-search 1.1%.
