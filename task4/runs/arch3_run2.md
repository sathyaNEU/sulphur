Reviewed 96 resources· 36m
Recommendation. Fire October scan alerts at Sosnowiec (HKTW), Strykow (HLDZ), and Pruszkow (HWAW).
Their missed-scan rates are 1.34%, 1.55%, and 1.23%, respectively, against the standard’s 1.00% tolerance. Each hub’s entire 90% interval is above tolerance. The other three hubs’ intervals are wholly below it.
Final answers. The hub results are in `tracking_scorecard_2026-10.xlsx`, on `Hub Scorecard`. Rates and interval bounds are displayed as percentages to two decimals; counts are whole numbers.

* Komorniki (HPOZ): 12,600 parcels handled; 61 missed sort scans; 0.48%, with 90% interval 0.39%-0.60%. No alert; wholly below tolerance.
* Bielany Wroclawskie (HWRO): 11,963 parcels; 95 misses; 0.79%, interval 0.67%-0.94%. No alert; wholly below tolerance.
* Sosnowiec (HKTW): 16,530 parcels; 222 misses; 1.34%, interval 1.20%-1.50%. Alert fires; wholly above tolerance.
* Modlniczka (HKRK): 13,628 parcels; 86 misses; 0.63%, interval 0.53%-0.75%. No alert; wholly below tolerance.
* Strykow (HLDZ): 12,178 parcels; 189 misses; 1.55%, interval 1.38%-1.75%. Alert fires; wholly above tolerance.
* Pruszkow (HWAW): 24,425 parcels; 301 misses; 1.23%, interval 1.12%-1.35%. Alert fires; wholly above tolerance.

The network reconciliation is 91,324 parcels = 90,370 with sort events + 954 missed sort scans.
The depot answers are on `Depot Scorecard`, in `Events sent twice` and `Never collected`. Replay counts cover the full courier extract, while noncollection counts cover latest-version October pre-advice parcels.

* D-POZ1, Poznan-Gluszyna: 581 events sent twice; 106 parcels never collected.
* D-POZ2, Leszno: 125 events sent twice; 257 parcels never collected.
* D-WRO1, Wroclaw-Pracze: 600 events sent twice; 162 parcels never collected.
* D-WRO2, Opole: 272 events sent twice; 139 parcels never collected.
* D-KTW1, Katowice-Zaleze: 324 events sent twice; 110 parcels never collected.
* D-KTW2, Bielsko-Biala: 375 events sent twice; 195 parcels never collected.
* D-KRK1, Krakow-Zablocie: 97 events sent twice; 43 parcels never collected.
* D-KRK3, Krakow-Rybitwy: 200 events sent twice; 86 parcels never collected.
* D-KRK2, Tarnow: 127 events sent twice; 170 parcels never collected.
* D-LDZ1, Lodz-Olechow: 599 events sent twice; 189 parcels never collected.
* D-LDZ2, Piotrkow Trybunalski: 292 events sent twice; 309 parcels never collected.
* D-WAW1, Warszawa-Okecie: 942 events sent twice; 145 parcels never collected.
* D-WAW2, Warszawa-Targowek: 736 events sent twice; 346 parcels never collected.
* Total: 5,270 events sent twice; 2,257 parcels never collected.

`scan_alerts_2026-10.pptx` contains the requested single-slide chart: every hub’s rate and 90% interval, the 1.00% tolerance line, and explicit FIRE / NO ALERT labels. Supporting counts and attribution qualifications are also included in its speaker notes.
Step-by-step process.

1. Established the governing rules and freeze. Read `TDS-4_tracking_data_standard.pdf` and `october_scorecard_request.eml` from the supplied ZIP. The applicable standard is v4.1, with a 1.00% tolerance. The freeze is 6 November 2026, 07:40 Europe/Warsaw, equivalent to 06:40 UTC. The standard fires alerts on the observed rate; the email separately requests independent-parcel 90% intervals.
2. Inspected all supplied sources. Used `depot_scan_events_2026-10.csv`, `hub_sort_events_2026-10.parquet`, `courier_events_2026-10.parquet`, and `edi_preadvice_2026-10.csv` for the measures. Used `network_register_2026-10.xlsx` for registered entities, scanners and replacement dates; `sort_plan_2026Q4.xlsx` for effective routes; and the 241 rows in `shipper_accounts_2026-10.csv` for integration-specific identifiers. Checked the 908 customer claims for contradictions. Inspected the 138 sorter-availability rows but did not use downtime as a parcel denominator, route identifier or proof of a scanner fault. File roles are documented on `Sources`.
3. Validated identifiers and dates. Preserved tracking identifiers as strings, including piece suffixes and `KW...PL` identifiers. Local timestamps were interpreted in `Europe/Warsaw`, including the October clock change. There were 0 whitespace corrections, invalid parsed timestamps, negative receipt lags or records excluded after the freeze. The 263,502 missing optional courier references were treated as empty references, not missing parcel identities.
4. Built the October hub population from unloading evidence. Removed 837 exact repeated arrival rows from 92,161, leaving 91,324 unique parcels, all unloaded in October. The 92,035 sort records covered 90,370 distinct parcels; the 1,665 additional sort records did not inflate parcel counts. This left 954 parcels without sort events. The parcel-level reconciliation is retained on `Hub Parcels`.
5. Assigned physical hubs rather than relying solely on the plan. Applied the route plan using the preceding sort night, including Opole’s move to Sosnowiec from 19 October, affecting 2,124 parcels and 31 misses. Observed sort labels then identified actual handling. For missing labels, used the unanimous observed hub within each delivery-depot, fixed-scanner and arrival-date cohort. All 300 cohorts had at least 16 scanned peers and no conflicting observed hub labels. The maximum within-cohort arrival gap was 42 seconds.
6. Resolved the material off-plan traffic. The Warsaw depots contained 24 off-plan cohorts with 1,440 parcels attributable to Strykow: 1,310 observed HLDZ scans plus 130 inferred missing scans. Every missing parcel had an observed peer within 18 seconds, and 945 of 954 misses were bracketed by observed peers. The cohort evidence and assignments are retained on `Unload Cohorts` and `Hub Parcels`.
7. Calculated rates and uncertainty. Computed missed scans divided by handled parcels, then two-sided 90% Wilson score intervals under the requested independent-parcel model. Wilson was preferred to the symmetric Wald interval for these low rates. Alert and interval comparisons use unrounded values. Exact Clopper-Pearson intervals produced the same tolerance-position conclusions for every hub.
8. Reconstructed logical courier scans. Grouped records using tracking identifier, named depot, courier, device, event code and canonical scan time, rather than transport IDs. The 280,378 records represented 275,108 logical scans, including 5,270 replayed scan groups. Replay matching found 101 exact-time, 3,088 local-minute-truncated, and 2,081 UTC-minute-truncated further records. Different genuine scan times remained separate. `Courier Replays` retains the original and further records for audit.
9. Selected the latest October pre-advice population. Removed 5,080 superseded versions from 89,067 rows, leaving 83,987 latest consignments representing 89,574 parcels across all dates. Then excluded 3,161 September consignments containing 3,356 parcels and 5 November consignments containing 6 parcels. October therefore contained 80,821 consignments and 86,212 parcels. Applied the D-KRK1-to-D-KRK3 replacement from 12 October, remapping 2,896 parcels.
10. Reconciled pieces, references and collection evidence. Expanded pieces individually, including the `001` suffix on single-piece EDI-B2B consignments. Matched marketplace references at the handheld’s 20-character width and counted distinct physical tracking IDs. The October population reconciles as 76,536 direct pickups + 7,419 handled without pickup scans + 2,257 never collected = 86,212 parcels. All 7,419 missing-pickup parcels had both downstream courier and depot-arrival evidence. Removing sort evidence changed 0 collection classifications.
11. Verified the outputs. All 73 analytical checks passed. Independent arrival-gap segmentation from 20 to 1,800 seconds preserved all hub assignments. Reopened both deliverables, checked archive integrity, cached formulas, percentage formats, slide bounds and the embedded chart, and reconciled the workbook’s detailed audit rows to every hub and depot total. Temporary analysis files were removed. A native Office rendering engine was unavailable; the embedded chart was visually inspected.

Assumptions and judgment calls.

* Missing hub origins are inferred, not manifest-proven. The homogeneous unloading cohorts strongly support the assignments, but the intervals do not incorporate attribution error. Holding observed origins fixed, Strykow’s alert fires if at least 63 of the 130 off-plan missing parcels belong to it. Reassigning 68 to HWAW would leave Strykow with 121 misses in 12,110 parcels, clearing its alert. That alternative is not supported by the observed peer labels or continuous unloading runs. This sensitivity is explicit in `Methods`, `Sensitivity`, and the slide notes.
* “Never collected” is an as-of-extract finding. It means no pickup or subsequent physical-handling evidence in the supplied frozen records, not a prediction about future collection.
* Partial reference matches remain unresolved individually. There are 67 never-collected parcels in 63 partially matched reference groups whose specific consignment identities cannot be established. Each group stays within one shipper, collection date and effective depot, so the depot totals remain determined.
* Replay timestamp repairs are evidence-based inferences. Repairs require an unambiguous match to an earlier scan with the same identifiers; broad time-window merging was not used.
* Intervals follow the requested parcel-independence model. They are individual hub intervals, not simultaneous network intervals or measures of shared equipment-failure uncertainty.

Alternatives rejected.

* Published plan as physical truth: would clear Strykow at 59 misses in 10,738 parcels, or 0.55%, but contradicts 1,310 observed HLDZ scans.
* October-only sort timestamps: would omit 1,465 parcels sorted before October for October unloading, creating false misses.
* October-only courier replays: gives 5,179, not the requested full-extract total of 5,270.
* Duplicate transport IDs or exact raw timestamps alone: produce 0 or 101 replay groups, missing the demonstrated timestamp variants. Grouping only by tracking identifier and status instead produces 10,108, collapsing genuine repeated scans.
* No pickup scan means never collected: produces 9,676 parcels, including 7,419 with positive later handling evidence.
* Filter October before replacing versions: retains 86,218 advised parcels, including 6 whose latest collection dates are in November.
* Clear an entire reference group after any pickup: reports only 144 reference-only noncollections instead of 211, hiding the remaining 67 in partial groups.
* Use the interval as the alert trigger: conflicts with TDS-4, which uses the point rate strictly above 1.00%.

Files produced.

* `tracking_scorecard_2026-10.xlsx`: hub and depot scorecards, methods, sensitivity analysis, source inventory, validation results and detailed reconciliation tables.
* `scan_alerts_2026-10.pptx`: single-slide hub rate-and-interval chart with fired alerts marked and supporting speaker notes.

Both files are saved under `/home/agent/workspace`.
Packages installed. The runtime lacked the advertised analytics libraries. Installed NumPy, pandas, SciPy, PyArrow, openpyxl, python-pptx, PyMuPDF, matplotlib and their dependencies, including XlsxWriter.
