Reviewed 89 resources· 29m
Recommendation. Fire October scan alerts at HKTW (Sosnowiec), HLDZ (Strykow), and HWAW (Pruszkow); do not fire alerts at HPOZ, HWRO, or HKRK.
The firing hubs’ missed-scan rates are 1.34%, 1.55%, and 1.23%, respectively, against the 1.00% tolerance. Their 90% intervals are wholly above tolerance. TDS-4 fires the alert on the unrounded point rate, not the interval.
Final answers. `tracking_scorecard_2026-10.xlsx`, Hub Scorecard, contains every hub’s handled parcels, missed sort scans, rate, 90% Wilson interval, tolerance comparison, and alert:

* HPOZ, Komorniki: 12,600 parcels; 61 missed scans; 0.48%; interval 0.39%-0.60%, wholly below tolerance; no alert.
* HWRO, Bielany Wroclawskie: 11,963 parcels; 95 missed scans; 0.79%; interval 0.67%-0.94%, wholly below tolerance; no alert.
* HKTW, Sosnowiec: 16,530 parcels; 222 missed scans; 1.34%; interval 1.20%-1.50%, wholly above tolerance; alert fires.
* HKRK, Modlniczka: 13,628 parcels; 86 missed scans; 0.63%; interval 0.53%-0.75%, wholly below tolerance; no alert.
* HLDZ, Strykow: 12,178 parcels; 189 missed scans; 1.55%; interval 1.38%-1.75%, wholly above tolerance; alert fires.
* HWAW, Pruszkow: 24,425 parcels; 301 missed scans; 1.23%; interval 1.12%-1.35%, wholly above tolerance; alert fires.

No hub’s interval crosses tolerance. The network totals are 91,324 handled parcels and 954 missed sort scans.
The workbook’s Depot Scorecard gives the requested depot exceptions. In each line below, the first count is courier events sent twice across the entire extract; the second is October pre-advised parcels never collected as of the extract:

* D-POZ1: 581 duplicated events; 106 never-collected parcels.
* D-POZ2: 125 duplicated events; 257 never-collected parcels.
* D-WRO1: 600 duplicated events; 162 never-collected parcels.
* D-WRO2: 272 duplicated events; 139 never-collected parcels.
* D-KTW1: 324 duplicated events; 110 never-collected parcels.
* D-KTW2: 375 duplicated events; 195 never-collected parcels.
* D-KRK1: 97 duplicated events; 43 never-collected parcels.
* D-KRK3: 200 duplicated events; 86 never-collected parcels.
* D-KRK2: 127 duplicated events; 170 never-collected parcels.
* D-LDZ1: 599 duplicated events; 189 never-collected parcels.
* D-LDZ2: 292 duplicated events; 309 never-collected parcels.
* D-WAW1: 942 duplicated events; 145 never-collected parcels.
* D-WAW2: 736 duplicated events; 346 never-collected parcels.
* Total: 5,270 duplicated events and 2,257 never-collected parcels.

`scan_alerts_2026-10.pptx` contains the requested single-slide chart: every hub’s rate and interval, a marked 1.00% tolerance line, and FIRE labels on the alerting hubs. Rates and bounds display two decimal places; counts in the workbook display as whole numbers.
Step-by-step process.

1. Read the supplied archive and governing documents. `TDS-4_tracking_data_standard.pdf` supplies the current definitions and tolerance; `october_scorecard_request.eml` supplies the extract context and independent-parcel interval requirement. The primary data comprise 92,161 depot-scan rows, 92,035 hub-sort rows, 280,378 courier rows, and 89,067 pre-advice version rows. The network register supplies hub/depot identities, replacement dates, door scanners, and handheld models; the sort plan supplies effective-dated routing. Shipper accounts were used for validation. The 908 customer claims and 138 sorter-availability rows were reviewed but not used to redefine the metrics: neither claims nor downtime determines whether a scan exists. These roles are recorded in Sources.
2. Fix the snapshot and validate identifiers and dates. The cutoff is 6 November 2026, 07:40 Europe/Warsaw, equivalent to 06:40 UTC. No supplied event receipt or EDI submission falls after it. Relevant date parsing and depot-code checks found no invalid dates or unknown depots. Missing optional customer references were not imputed. EDI has 17,852 missing barcodes and 71,215 missing references, but no record lacks both identifiers. Courier events have 263,502 missing optional references. Details appear in Methods and Checks.
3. Construct the October hub population. Removed 837 exact arrival repeats, leaving 91,324 distinct physical parcel barcodes unloaded in October. Full piece barcodes remain separate parcels. Sort events were reduced to presence by barcode: 90,370 parcels have a sort event, leaving 954 missing. The additional 1,665 sort-event records do not add parcels. October membership comes from unloading date, not sort-event date; this retains 3,427 parcels unloaded on 1 October. Evidence is retained in Hub Parcels.
4. Resolve actual hub routing. Matched the effective sort plan using delivery depot and unloading date minus one day. Then examined the observed hub within each depot, sort night, and door scanner. All 300 groups contain exactly one observed hub, supported by at least 16 scanned parcels. Crucially, 24 Warsaw unloading groups across 12 nights contradict the published plan: 1,310 observed parcels identify HLDZ, and their groups contain another 130 parcels missing sort scans. Assigning the whole unloading groups to HLDZ moves 1,440 parcels from planned HWAW routing. Routing Evidence documents every group.
5. Calculate rates and intervals. For each hub, divided missing scans by handled parcels and calculated a two-sided 90% Wilson binomial interval. Wilson was chosen over a simple Wald interval because it is better suited to small proportions. The requested independent-parcel model determines the primary intervals; comparisons use full precision before display rounding. An independent calculation reproduced the results, and exact binomial intervals gave the same tolerance classifications. Hub Scorecard, Methods, and Hub Sensitivity contain the calculations and interpretation.
6. Reconstruct courier events sent twice. Retained the entire extract, as requested. Every courier transport event ID is unique, so ID equality cannot identify replays. Matched barcode, event-named depot, courier, device, event type, reconstructed scan minute, and later receipt. TC52 replays truncate the local timestamp to the minute; TC51 replays encode the UTC minute and require conversion to Warsaw time. This yields 275,108 underlying scans: 269,838 received once and 5,270 received twice, with no ambiguous matches. The duplicated scans comprise 85 September, 5,179 October, and 6 November events. Courier Retry Audit retains every matched pair.
7. Resolve the collection population before matching. Removed 5,080 superseded pre-advice rows, leaving 83,987 latest consignments. Only then filtered collection dates, excluding 3,161 September consignments representing 3,356 pieces and 5 November consignments representing 6 pieces. The October population is 80,821 consignments and 86,212 parcels. Applied the Krakow replacement from 12 October 2026, reassigning 2,896 parcels, including 47 never-collected parcels, from D-KRK1 to D-KRK3. Latest Preadvice retains the selected versions and effective depot assignments.
8. Match individual parcels and reference buckets. Numeric piece barcodes were matched to their consignment family while retaining distinct full barcodes for counts. This resolves 70,055 expected barcode-bearing parcels into 68,009 collected and 2,046 missing. Reference-only consignments were reconciled using the handheld’s retained reference representation, including truncation to 20 characters: 16,157 expected parcels, 15,946 collected, and 211 missing. Buckets were checked for consistent account, depot, and collection date; none was overmatched. Partial consignments remain partial: 340 consignments contain 382 missing pieces. Collection Ledger records these reconciliations.
9. Use all positive collection evidence and verify the files. Pickup, downstream courier events, depot arrival, and hub sorting can establish physical handling; `PICKUP_FAILED` alone cannot. Positive courier evidence and depot arrivals independently identify the same 91,324 parcels. October collection therefore reconciles to 86,212 advised = 83,955 collected + 2,257 missing. The evidence population also reconciles to 83,955 October matches + 3,271 September matches + 4,098 unmatched parcels; unmatched parcels were not allocated speculatively. Reopened both deliverables and checked cached formulas, totals, percentage formats, audit-sheet row counts, slide text, shape boundaries, and archive integrity. Removed the temporary build script.

Assumptions and judgment calls.

* Missing-scan hub attribution is inferred from unloading peers. The evidence strongly supports the depot-door-night assignment: 945 of the 954 missing parcels fall within their group’s observed arrival span, and the remaining 9 are no more than 10 seconds outside it. Nevertheless, this is not direct observation of the missing sort event.
* Strykow’s attribution matters to the decision. Reassigning 68 or more of the 130 disputed missing parcels from HLDZ to HWAW would remove HLDZ’s alert. The observed hub consistency and arrival timing support retaining them at HLDZ. This limitation is explicit in Methods, Hub Sensitivity, and the slide notes.
* Intervals do not incorporate routing uncertainty. They implement the requested independent-parcel model. A whole-night resampling sensitivity check gave 1.21%-1.47% for HKTW, 1.11%-1.99% for HLDZ, and 1.01%-1.45% for HWAW. The classifications remain above tolerance, although HWAW becomes close.
* “Never collected” is a snapshot conclusion. It means no matched positive collection evidence by the fixed extract. It cannot exclude completely unrecorded physical collection or collection after the snapshot.
* Reference truncation supports aggregate counts, not arbitrary individual identification. Missing quantities within partially collected reference buckets can be assigned to the correct depot, but individual missing consignment identities cannot always be recovered.
* EDI availability relies on the supplied snapshot. EDI provides submission time rather than platform receipt time; latest-version selection therefore uses the supplied extract, with submission timestamps checked against the cutoff.

Alternatives rejected.

* Published plan alone: would give HLDZ 0.55% and HWAW 1.67%, but contradicts 1,310 observed HLDZ-scanned parcels. Assigning observed parcels to HLDZ while leaving their missing unloading peers at HWAW is also unsupported by the group evidence.
* Interval lower bound as the trigger: TDS-4 specifies the monthly point rate above 1.00%. The interval is supporting uncertainty information, not a replacement rule.
* October-only courier counts: would report 5,179, omitting the extract’s 85 September and 6 November duplicated scans.
* Transport-ID deduplication: would find no repeats because all 280,378 courier IDs are unique; timestamp reconstruction identifies the source replays.
* Missing pickup event means never collected: would report 9,676 parcels. Of these, 7,419 have downstream handling evidence, leaving the supported count of 2,257.
* Literal full-reference matching: would report 7,595 missing parcels, failing to recover 5,338 collected parcels whose references were truncated.
* One observed piece satisfies the whole consignment: would report 1,875 missing parcels, losing 382 missing pieces from partially collected consignments.
* First pre-advice version: would report 2,263 missing parcels, wrongly retaining 6 parcels revised to November.
* Downtime or claims as the deciding explanation: neither changes the standard’s scan-presence test. The results justify audits, not a causal diagnosis of equipment failure.

Files produced.

* `/home/agent/workspace/tracking_scorecard_2026-10.xlsx`: hub and depot scorecards, parcel-level and retry evidence, latest pre-advice, collection reconciliation, methods, sensitivity checks, and source inventory.
* `/home/agent/workspace/scan_alerts_2026-10.pptx`: single-slide, editable rate-and-interval chart with the tolerance and firing hubs marked, plus explanatory speaker notes.

Packages installed. pandas, NumPy, SciPy, openpyxl, python-pptx, PyArrow, pypdf, matplotlib, XlsxWriter, and their dependencies. They were installed in an isolated temporary package location because the advertised analytics packages were unavailable in the active interpreter.
