# Determinism check, pass 2 (task13)

Scope: the two shipped changes since pass 1 (routine rows of `vegetation_work_orders_2022-2026.csv` near designed
places now read MOWING instead of HERBICIDE or HAZARD TREE; Supplementary Question 6's addressee wording). Gates A
to E only.

## Verdict

**DETERMINISTIC.**

## Disposition

**APPROVE**, with one optional, non-blocking wording note on Supplementary Question 6 (see Fix).

## What changed and whether it moves anything

Re-extracted `target.zip` fresh and read `vegetation_work_orders_2022-2026.csv` end to end against every structure
and span the answer blocks name.

**The three entries that actually decide a fixed/unfixed call are untouched, and could not have been touched by
this edit.** All three are `HOT SPOT` work orders ("trim tree after contact"), the type the data generator uses for
an actual tree-to-conductor contact trim, not `HERBICIDE` or `HAZARD TREE`:

| Location | Row in current file | Still present, unchanged |
|---|---|---|
| Line 5, structure 102 (Supplementary 4, fixed, vegetation grown into the line) | 2026-06-08, Line 5, 101-102, HOT SPOT | yes |
| Line 14, structure 131 (Supplementary 4, fixed, vegetation grown into the line) | 2026-06-13, Line 14, 131-132, HOT SPOT | yes |
| Line 6, structures 57-58 (Critical Component 2, the oak cut back 9 Aug 2022) | 2022-08-09, Line 6, 57-58, HOT SPOT, "trim tree after contact" | yes |

Since the described edit only touches rows that were `HERBICIDE` or `HAZARD TREE` and now read `MOWING`, and none of
the three deciding rows are either of those types, none of the three defining facts in Critical Component 2 or the
Supplementary 4 fixed list could have moved. Reproduced: the oak-cutback date (9 Aug 2022) and the "every summer
since" trajectory in Component 2 stand; both fixed-grow-in entries stand.

**The rows that did change are all non-deciding, and the procedure text rules MOWING out as a fix either way.**
Found MOWING rows overlapping named locations at: Line 7/38 (bird, 2023-02-04 and 2026-02-23), Line 11/40
(insulator, 2023-09-25), Line 13/72 (insulator, 2026-10-09), Line 14/62-63 (grow-in span, still to clear,
2023-10-13 and 2024-02-01), Line 13/103-107 (hazard-tree stand, still to remove, 2025-01-16). None of these matter:

- The bird and insulator-failure locations are fixed (or not) by `line_maintenance_work_orders_2022-2026.csv` (perch
  guards, string replacement), a file this edit did not touch; vegetation work orders are irrelevant to their cause.
- `reliability_reporting_procedure_rev4.docx` section 2 defines the fix for each cause explicitly: "clearing the
  span for vegetation grown into the line; removal of the hazard trees for vegetation from outside the right of
  way." MOWING ("mow right of way") is neither; it is routine grass control, not a tree trim or removal. A careful
  reader is pinned by this definition and cannot credit a MOWING row as the fix for a grow-in span or a hazard-tree
  stand regardless of its type before or after the edit. Checked: no `HAZARD TREE` or `CYCLE TRIM`/`HOT SPOT` row
  sits at Line 11, structures 118-120 or Line 13, structures 103-107 (the two still-outstanding stands) in the
  current file, so both remain correctly unfixed, matching "remove the hazard trees at 2 dead pine stands" in the
  Final Recommendation and the "2 stands" in Step-by-Step 7. Line 14, structures 62-63 likewise carries no
  qualifying trim after its repeat faults and remains on the "clear 4 grow-in spans" list.

No repeat location's fixed/unfixed call, and no figure in Supplementary 4 or Critical Component 2, moved. This
matches the author's statement that no graded figure changed.

## Supplementary Question 6 wording (addressee)

Re-read `reliability_reporting_procedure_rev4.docx` (the only file naming reporting roles) and grepped every shipped
file (csv, and the XML inside every xlsx/docx, and `strings` on both PDFs) for "environmental" and "compliance":
zero hits anywhere in the package. The procedure names System Protection, the system operators, the line
superintendent, the vegetation management coordinator, the line crews and the Manager of Engineering (the
approver). "Environmental compliance" as a recipient of the memo is not grounded in any shipped file.

This is not a decisive fact the call turns on, and it is not the recommended action's vocabulary (Gate B's
sharpest failure mode): it is one clause describing who the one-page memo is addressed to, a formatting detail of
Supplementary Question 6, not a figure any run is graded on reproducing numerically. It does not reach Gate B, C,
D or E as a determinism failure on its own; it is a loose end worth tightening, not a fork that produces a
different committed answer (no file licenses an alternative addressee list a solver could defensibly substitute
that changes any number).

## Evidence summary

| Item | Blocks' value | Reproduced on current files |
|---|---|---|
| Line 5, structure 102 fix (grow-in) | fixed, HOT SPOT 2026-06-08 | yes, unchanged |
| Line 14, structure 131 fix (grow-in) | fixed, HOT SPOT 2026-06-13 | yes, unchanged |
| Line 6, structures 57-58 oak cutback | 9 Aug 2022, HOT SPOT | yes, unchanged |
| Line 11, structures 118-120 (hazard-tree stand) | unfixed | yes, no qualifying WO of any type |
| Line 13, structures 103-107 (hazard-tree stand) | unfixed | yes, no qualifying WO of any type |
| Line 14, structures 62-63 (grow-in span) | unfixed, on the clear list | yes, only MOWING/old CYCLE TRIM, no qualifying fix |
| Line 10 47-48, 88-89; Line 11 64-65 (grow-in spans) | unfixed, on the clear list | yes, only pre-dating CYCLE TRIM, no post-fault fix |

Alternative run: a solver who, against the procedure's own definition, credited a MOWING row as "clearing the
span" would still land on the same unfixed calls here (none of the changed MOWING rows sits where it would flip a
currently-fixed location to unfixed, or vice versa), so even the unreasonable reading does not move the list.

## Fix

**Location: none** for determinism (Gates A-E pass; no graded figure, Critical Component or repeat-location call
moved by the shipped file edit). **Location: solution** (optional, cosmetic) for Supplementary Question 6: replace
"environmental compliance" with a recipient the files actually name (e.g. drop it, or use "System Protection"),
or add one line to `reliability_reporting_procedure_rev4.docx` naming an environmental-compliance role if the
author wants to keep it. Not required before ship; it does not touch a graded figure or the call.
