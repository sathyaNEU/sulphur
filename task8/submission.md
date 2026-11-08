## Tags

**Domain:** Education & Learning Sciences (item response theory and test equating: an adult numeracy awarding body pre-equating its 2027 Level 1 paper from its Rasch item bank).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Set the 2027 Level 1 Numeracy pass mark at 19 of 40: a candidate who just meets the standard can be expected to score 19.09 on the paper once its twelve Level 2 patterns and relationships items carry the reading cost Level 1 candidates pay on long stems; the bank's own values give 21.57 and a pass mark of 22, which this rejects.**

## 2. Supplementary Questions

1. pass_mark_2027.docx: a memo to the Awards Committee recommending a pass mark of 19 of 40, stating the expected mark of 19.09 at the standard (26 of 40 on the 2022 paper) against the bank's 21.57, and why the twelve patterns and relationships items are harder for Level 1 candidates than their bank values.
2. l1_2027_items.xlsx, item table: one row for each of the 40 items on the 2027 paper with its chance at the standard (two decimals) and whether it sits inside the 0.20 to 0.90 band. Five of the twelve patterns and relationships items (Q29, Q30, Q31, Q32, Q33) sit below the band, at 0.11 to 0.14; the other seven sit inside it at 0.25 to 0.40; no item sits above the band.
3. l1_2027_items.xlsx, regions: the mean mark the candidates who sat the 2026 Level 1 paper in each region could be expected to score on the 2027 paper (whole marks): Winnipeg 15, Westman 16, Interlake-Eastman 17, Parkland and North 16, Saskatoon and Central 17, Regina and South 17.

## 3. Critical Components

- The bank's final 2026 values put the 2027 paper's expected mark at the standard at 21.57 (pass mark 22); they carry the twelve patterns and relationships items at difficulties set by Level 2 candidates.
- On the 36 Level 2 items the 2023 to 2026 Level 1 papers carried, each item's Level 1 difficulty less its Level 2 difficulty needs two causes together: an everyday-context advantage of about 0.9 logits and a reading cost of about 0.8 logits per 100 words of stem. On the long everyday items the two cancel (their shift sits -0.20 logits from the short mathematical items', the short everyday items' -0.83).
- The twelve patterns and relationships items are long and mathematical, so only the reading cost applies: at the standard they are worth 2.82 marks against 5.29 on the bank's values, and five of them fall below the band.
- Expected mark at the standard on the 2027 paper: 19.09, so the pass mark is 19.

## 4. Step-by-Step Solution

1. Conform the response export: map the 2022 and 2023 sittings' positions (Q01 to Q40) to bank codes through the paper layouts, keep the later answer of every item answered twice after a reconnect, and attach each sitting to its paper; count each register sitting once.
2. The bank's final 2026 run gives 21.57 at the standard on the 2027 paper; screening the shared items the usual way (link through them, set aside the outliers) flags the short everyday items and leaves the rest looking unchanged, which still files 21. That reading is rejected.
3. Calibrate the Level 1 sittings and the Level 2 sittings each on their own (Rasch) and take, for each of the 36 Level 2 items set on Level 1 papers, its Level 1 difficulty less its Level 2 difficulty.
4. The short everyday items are easier for Level 1 candidates and the long everyday items are not, so a second cause offsets the everyday advantage on the long ones: fit the shift on an intercept (the link), the stem's length and the context together. Context alone (20.81 at the standard) or length alone (21.35) leaves one kind of item misfitting.
5. Give each 2027 patterns and relationships item its Level 2 difficulty plus the link and the reading cost for its stem; the Level 1 items keep their Level 1 values.
6. Find the ability at which the 2022 paper's expected mark is 26 and sum the 2027 paper's chances there: 19.09, so the pass mark is 19; the item chances and the band follow from the same ability.
7. Regions: join each 2026 Level 1 sitting to the register's sitting centre (one row per candidate) and the centres list. The 2026 paper is heavy in everyday items and the 2027 paper light, and the regions differ in how much easier everyday items are for their candidates, so estimate each region's own everyday deviation on the Level 1 sittings, each candidate's ability on the 2026 paper with it, and average the expected 2027 marks by region; one ability scale for every region files other whole marks in some regions.
No other reading survives: every route that leaves the 2027 items on their Level 2 values, credits only the everyday advantage or prices only stem length files 21 or more, and every form of the two-cause model (linear, logarithmic or a long-against-short step in stem length, weighted or not) files 19.
