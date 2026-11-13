# leak check, task9

**Verdict: REVIEW.** 29 files read, 47 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: missed, result, loading, method, shortcut, carried, yields, slurry, controller, points, cleans, independent, window, quarter, counter, polymer, die-area, conditions, component, attribution, database, effect, formula, export, change

## 1 file names (REVIEW 1)
- **REVIEW** `shift_handover_ft2_2026.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `vr90_ramp_plan_q1_2027.pdf`: golden figure 300 appears: ...no change. ILD0 deposition, DP1 to DP3 DP2B on SH-300-C since its replacement of 6 April 2026, the othe...
- **REVIEW** `vr90_ramp_plan_q1_2027.pdf`: carries 25 of 34 distinctive words of the committed call: "Before VR90's first lots reach these steps, restore the oxide slurry loop's flow, put the pre-gate bench back on its spr"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `shift_handover_ft2_2026.txt`: 4 of 25 stump-paragraph terms appear (slurry, controller, export, change); read whether the document names the move
- **REVIEW** `vr90_ramp_plan_q1_2027.pdf`: 5 of 25 stump-paragraph terms appear (slurry, cleans, quarter, conditions, change); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 29 usable files (10 or more required)
- **INFO** `-`: 4 file categories: database, document, spreadsheet, structured (2 or more required)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### Read 1 (2026-11-13, isolated Sonnet reader at medium, the pack before the house pass)

1. Method-telling text: none that dictates a step. The prompt says "VR90 has never been sorted here and no record says which die each cause killed, so both answers have to be estimates" (that the answer is an estimate, not how), gives the comparison windows and the per-cause quantities asked. The ramp plan fixes operating conditions ("P-02A on the EP-114 setpoint of 38 Hz", "ECN-2026-0417 ... as today", "Operations will set the quarter's wafer starts from the sort yield agreed"); these are conditions, not methods; "Each bench is planned at 31 lots a day with VR90 and the Q1 product mix" is a loading input.
2. Ranking or scoring file: none. The cost inputs carry EUR per die and savings, no ranking.
3. Files that exist only to help: none clearly; the product sheet and the cost inputs are reference inputs; possible distractors named: the cleanroom environment, the overlay lots, the probe-card touchdowns, the lot genealogy, the facility line list.
4. Reads as the answer: nothing numeric; closest are the filed change events that line up with the causes (ECN-2026-0417, FC-2026-034, the recipe log's R8 zone 5) and the ramp plan's section 3 table, which names the cause areas and their conditions in one table: context, but a solver reads the candidate set straight off it.
5. Filed sentences that fix a figure or population: the design-limited fallout at 1.9 per cent (consistent with the product sheet's 0.981); the back-end yields 99.2 and 98.1 per cent and 184 gross die; the commitment in final good units (back-end losses between sort and delivery); CM3 back on R7 before VR90's first ILD0 lot (no CM3 R8 effect for VR90 under the plan); VR90 at 21 per cent of each deep-etch chamber's wafers; 12 lots a week until the yield is agreed.
6. One thing that settles most of it: none found; closest is the plan's section 3 table, which says what each cause area runs under for VR90 and so what "as filed" means, without yields or per-die costs. Per part: the causes, the ranking and each cause's cost turn on analysis; the shortfall is data reading with re-probe insertions handled; each fix is mostly read from the filed documents; VR90's fixed yield is analysis (transfer to a larger die and another etch recipe); each fix's VR90 add and the plan yield are analysis on the plan's conditions; the wafer starts are arithmetic.

Sweep lines: the shift book harmless (the shift book's own log); the plan's figure overlap harmless (filed inputs the plan owns); the plan's shared words harmless (conditions and an open item, no fix or effect; mild note that the table doubles as a list of the cause areas); the ECN register's dates harmless (effective dates of approved changes).

Realism tells: (1) the ECN register small and curated around the story; (2) the shift book's routine lines repeated verbatim, the story entries the only ones with weight; (3) lot IDs changing format partway; (4) the recipe log's "fleet alignment" on every follow-on row; (5) one person on every facilities entry and one analyst on every lab result.

Main thread's rulings on read 1: questions 1 to 5 harmless, every question 5 sentence executes to the golden. Question 4's and 6's table: the plan's section 3 now lists all twelve areas VR90 runs through, so it no longer reads as a list of the causes; the conditions stay, as the WHAT of "under the ramp plan as filed". Realism tells 1 to 5 fixed in the generator (31 ECNs in raised order across the fab's areas; the shift book written from the floor's events with a crew rota; the MES cut-over's ECN and shift-book line; the engineers' own reasons; three facilities people and a two-analyst lab rota). Because documents changed, the pack is read again (read 2).

### Read 2 (2026-11-13, isolated Sonnet reader at medium, after the house pass)

1. Method-telling sentences: none in the prompt; the ramp plan's "Operations will set the quarter's wafer starts from the sort yield agreed at the ramp readiness review; until then the 12 lots a week stand" and "Each bench is planned at 31 lots a day with VR90 and the Q1 product mix" are plan content, not method; the ECN register and recipe log carry dated changes, facts not instructions.
2. Ranking or scoring file: none; bin_def lists bin names and good flags only; no cause-level attribution anywhere.
3. Files existing only to help: none evident; the product sheet and cost inputs are reference inputs; several files look like distractors or supporting evidence, none carries a conclusion.
4. Answer-like figures: the plan's inputs (1.9 per cent design-limited fallout, 99.2 and 98.1 per cent back end, 412,000 units, 12 lots a week, 184 gross die, 21 per cent share) and the cost inputs, context that prices the fixes; nothing reads as a finished answer.
5. Filed sentences that fix a computation literally: CM3 back on R7 before VR90's first ILD0 lot (the CM3 recipe cause already fixed for VR90 under the plan); T3 on ECN-2026-0417's life, P-02A at 38 Hz, SH-300-C kept and cleans at 2,400 wafers (those causes stay in the plan as filed); the design-limited 1.9 per cent with the product sheet's 0.981; the back-end yields converting good die to units; Q1 2027 sorting for the commitment; both windows fixed by sort date.
6. One-thing check: no single file settles most of the work; the plan says which causes are fixed or not under the plan as filed and the ECN register and facilities log date the changes, each leaving the attribution, the VR90 transfer and the starts to be worked out. Per part: the shortfall is analysis with assembly; the ranking and costs are analysis; VR90 with every cause fixed is analysis plus reading the 1.9 per cent; each fix's add under the plan and the plan's yield are the transfer analysis on top of the plan's stated conditions; the starts are arithmetic.

Sweep lines: the shift book harmless (the shift book's own export, four crews' initials, downtime, pad changes, re-probes, holds; describes no data); the plan's shared figure harmless (the plan's own inputs); the plan's shared words harmless (conditions per area and the open item, never what to change); the plan's column-name echoes harmless (a controlled document with number, owner, issue date, distribution and revision); the ECN register's dates harmless (effective dates of approved future changes, consistent with the plan).

Realism tells: (1) the CM3 zone 5 tune in the recipe log and ECN-2026-0466 restoring it read as a neatly paired cause and fix (mild); (2) the register's statuses all closed or approved on a clean cadence (mild); (3) the shift book's four leads near-equal in count, its routine phrases templated; (4) the lot ID format change a staged join hurdle, though documented by ECN-2026-0326, and the genealogy small; (5) the facilities log's SDS-OX1 entries and the lab's extra samples line up with the investigation window, the lab sheet reading as a file carrying one fact.

Main thread's rulings on read 2: questions 1 to 5 harmless, every question 5 sentence executes to the golden. Question 6's "the plan's stated conditions" is the WHAT of "under the ramp plan as filed" (filed by design); the careful but hurried pass reads the same conditions and lands at 52.1 per cent against 45.4, so the parts turn on the transfer analysis, not on the reading. Tell 1 harmless: a recipe tune after a 49-site review and the fleet harmonisation raised months later is a recipe's ordinary life, and the harmonisation is the plan's own change the edge result tests. Tell 2 fixed: the register now carries a withdrawn and a rejected change beside the one in review. Tell 3 harmless: four crews on an eight-day rota log near-equal shares, and a shift book's routine entries are formulaic. Tell 4 harmless: the cut-over is the MES's own event, documented where an MES change is (the ECN register and the shift book). Tell 5 harmless: the lab workbook is the T3 bath programme's results, 86 routine weekly samples across the year on both benches beside the investigation's 30, and the SDS-OX1 entries are the facilities log's own record among its 25 entries; adding other tanks' rows to the lab file was weighed and refused, because an unfiltered read of the tank column would then move R3, a field-reading trap the house rules forbid.

### Read 3 (2026-11-13, isolated Sonnet reader at medium, after the read 2 and judge pass 2 repairs)

1. Method telling: no sentence dictates a method; the closest are the plan's operating conditions and planning conventions (the starts set from the agreed yield, Q1 2027 sorting for the commitment, the back-end yields, 184 gross die); the prompt pins the question, not a step; the plan's section 3 names the areas, and the ECN register and recipe log date a change per area.
2. Ranking or scoring: none.
3. Helper-only file: the cost inputs nearest (only costs and power figures for the candidate fixes); the ECN and facilities logs ordinary records.
4. Reads as answer: no number or name; the cost rows and ECN-2026-0417's saving name the candidate fix areas, not a ranking or a yield.
5. Filed sentences: CT-DEEP-07 on ET1B and ET3A at about 21 per cent with cleans at 2,400 wafers; T3 on ECN-2026-0417's life at 31 lots a day; P-02A at 38 Hz; CM3 back on R7 before VR90's first ILD0 lot, ILD0-VR on CM1 and CM3 only; "both chambers of each tool on the qualified SH-300-C showerhead"; 184 gross die and the back-end yields; the 1.9 per cent design-limited fallout; 12 lots a week until the yield is agreed; ECN-2026-0480's dispatch.
6. Single thing: none; the plan's conditions table orients the cause list but gives no magnitude, no cause-to-bin mapping and no VR90 transfer. The causes, the shortfall, the ranking and VR90 with every cause fixed are analysis; each fix's add and the plan yield are analysis with the plan's stated exposures; the starts are arithmetic.

Sweep lines: all harmless (the shift book the plant's own record; the plan's figures its own inputs; the plan's shared words conditions and an open item; the plan a controlled document; the ECN dates approved future effective dates).

Realism tells: (1) the plan, issued 30 October, cites ECN-2026-0487, approved 3 November in the register; (2) the extracts' export times one morning's session at 1 to 5 minute steps; (3) the shift book's four leads near-equal and its templated sentences; (4) the cost inputs read as a file prepared to price the five fixes, with key names closer to a task spec than a controller's sheet; (5) the ECN register very clean, each date chain lining up with a change in the other files.

Main thread's rulings on read 3: questions 1 to 4 and 6 harmless. Question 5's showerhead sentence, read literally, put all six chambers on SH-300-C against the PM log's one replacement: fixed (the plan now files DP2B on SH-300-C since 6 April, the other five on SH-300-B, and no replacement due before the end of Q1 2027), the same fork as judge pass 2's F1. Tell 1 fixed (ECN-2026-0487 approved 28 October, the register saved 4 November after its last entry). Tell 2 harmless: the extracts are the yield team's pull of 6 November, one analyst exporting each system in turn. Tell 3 harmless as ruled on read 2. Tell 4 fixed: the cost inputs are now controlling's 2027 planning sheet (energy with the audited drives, chemicals, spares, downtime and labour rates, die values and wafer costs), the fixes' inputs among them. Tell 5 harmless: a change-control export is clean by construction, and it now carries a withdrawn, a rejected and an in-review change beside the closed ones.

### Read 4 (2026-11-13, isolated Sonnet reader at medium, after the re-judge's repairs)

1. Method text: none; the prompt says estimation is needed, not how; the plan's starts convention, back-end yields, gross die and the commitment's definition fix the conversion, not a method.
2. Ranking or scoring: none; bin_def lists bin names only.
3. Helper-only file: none; the product sheet and the plan are context documents, the ECN register a change register.
4. Reads as the answer: none; candidate causes appear only as raw material (ECN titles, the facilities and recipe logs); the 1.9 per cent design-limited fallout is a stated input matching the product sheet.
5. Filed sentences: the back-end conversion and 184 gross die; Q1 2027 sorting; 12 lots a week as filed; T3 on ECN-2026-0417's life at 31 lots a day; ILD0-VR qualified on CM1 and CM3 only, dispatched by today's bay rules; CM3 back on R7 on 23 November; DP2B on SH-300-C with no replacement due before the end of Q1 2027; CT-DEEP-07 on ET1B and ET3A at about 21 per cent with cleans at 2,400 wafers; the 1.9 per cent design-limited fallout.
6. One thing: none; the plan's section 3 settles which VR90 conditions apply, not any yield, the VX40 and VP12 attribution or the ranking. Per part: the shortfall is analysis with assembly (the lot ID change, re-probe insertions); the ranking and fixes are analysis; VR90 with every cause fixed reads the stated design-limited figure plus the plan's conditions; each fix's add and the plan yield are analysis with a careful read of the plan; the starts are arithmetic on the prior result. Nothing looks planted.

Sweep lines: all harmless (the shift book's own export; the plan's own inputs; the plan's conditions only, nothing saying what to change; the ECN effective dates).

Realism tells: (1) the shift book's four sign-offs near-equal and templated phrasings; (2) the product sheet's blank row before the lone VR90-T engineering row; (3) the recipe log's sixteen tidy one-line reasons; (4) the lot ID format, documented in the ECN and plausible; (5) the line list's February save time.

Main thread's rulings on read 4: questions 1 to 6 harmless. Question 5's "every cause fixed leaves only the design-limited fallout" is the reader's gloss, not a filed sentence: the causes are the causes of the June to September fall the prompt names, and the answer blocks carry the random-defect, scratch, gate oxide and edge parts that remain. Tells 1, 3 and 4 harmless as ruled before. Tell 2 harmless: the product engineering sheet lists production products and then its engineering vehicle, and VR90-T's row is the line's only process record of VR90's die, recipe and RF time, which every VR90 result needs. Tell 5 harmless: the facility line list is a static drawing register last revised in February.
