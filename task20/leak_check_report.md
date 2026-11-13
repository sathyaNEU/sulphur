# leak check, task20

**Verdict: REVIEW.** 18 files read, 30 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, architecture, quarter, contract, missed, affiliate, careful, dropped, prototype, second, result, hardening, clearing, licence, points, engine, deposits, written, storage, notices, hurried, policy, method, golden, inside

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `hallingvass_regulation_licence_extract.pdf`: 3 of 25 stump-paragraph terms appear (second, licence, storage); read whether the document names the move
- **REVIEW** `hk_hedging_policy_2025.docx`: 4 of 25 stump-paragraph terms appear (second, clearing, points, policy); read whether the document names the move
- **REVIEW** `hk_liquidity_standard_2026.pdf`: 4 of 25 stump-paragraph terms appear (record, contract, clearing, licence); read whether the document names the move
- **REVIEW** `nex_clearing_margin_summary.pdf`: 3 of 25 stump-paragraph terms appear (quarter, clearing, notices); read whether the document names the move

## 9 dates after the setting (REVIEW 5)
- **REVIEW** `hk_sales_ledger_2018_2026.csv`: 4 ISO dates after 2026-12-31, e.g. 2027-01-02
- **REVIEW** `hk_supply_contracts_register.xlsx`: 2 ISO dates after 2026-12-31, e.g. 2028-12-31, 2029-12-31
- **REVIEW** `nex_daily_settlement_2018_2026.csv`: 8554 ISO dates after 2026-12-31, e.g. 2027-01-01, 2027-01-31, 2027-02-01, 2027-02-28, 2027-03-01
- **REVIEW** `nex_dayahead_settlements_2018_2026.csv`: 2 ISO dates after 2026-12-31, e.g. 2027-01-04
- **REVIEW** `nex_positions_month_end_2017_2026.csv`: 56 ISO dates after 2026-12-31, e.g. 2027-01-01, 2027-12-31, 2028-01-01, 2028-12-31

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 18 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Read: prompt.txt, all 27 target files (heads, labels only on the large CSVs, the PDF, the xlsx cell by cell, a sample of releases plus greps across all 19). Nothing solved or computed.

**1. Sentences that say how to do part of the analysis.**
- Prompt: "The card panel is the only read on the quarter before then, and it is a sample of cardholders, not the company's books, so the answer has to be an estimate." This names the panel as the input and the estimate as the form; it does not name a step. Harmless context.
- Prompt: "short if the whole range sits below the street's figure, long if it sits above, otherwise no position." This is the decision rule (a stated convention). Fine.
- larkhill_bmh_card_model_q3fy25.xlsx, Fit sheet, A6 to A8: "Per-card spend: Kestrel spend per open panel card, merchant ids M0412, M0413 and M2290 (from 2 June 2024) as delivered, issuers in the panel in both quarters, weekly averages." / "Reported growth: net sales per week, Fernhollow taken out unless in both quarters." / "Fit: least squares, fiscal 2022 Q1 to fiscal 2025 Q2. Back-test: from the seventh quarter, each fitted on the quarters before it." This is a prior analyst's method note and does hand over a recipe (merchant set, panel-constancy rule, per-week normalisation, Fernhollow treatment, fit window, back-test design). It is the largest leak surface; see Q5 and Q6.
- 10-K PDF: "Brindle & Moss shop-in-shops in Hollister's department stores and the Brindle Cafe locations are operated by licensees ... Their sales are not our net sales" and "Fernhollow Outfitters, acquired in fiscal 2024 ... consolidated from the date of acquisition", "Fiscal 2023 was the 53 weeks ... its fourth quarter had 14 weeks." These are company-disclosure facts that tell which merchants and weeks count. They describe the entity, not a step, but they do point at which descriptors to exclude and the week-count adjustment.

**2. File that already ranks/scores candidates.** None rank candidates. bmh_q4fy25_street_estimates.csv lists broker estimates (about 1506 to 1532) and ratings; it is the comparator the prompt names, not a ranking of an answer. The xlsx "Q3 FY2025 call" sheet is a prior call on the previous quarter (model 1333.7 vs reported 1306.9), not on this question.

**3. Files that exist only to help the analyst.** None is a data dictionary or readme. The xlsx Fit sheet notes (A6:A8) and the 10-K excerpt are the nearest to helper documents, as above. The delivery-history CSV (a vintage log of what the panel delivered on each date) is a data file, not a note.

**4. Figure or name reading as the answer.** No quarter-level Q4 FY2025 net sales figure appears anywhere. The xlsx has a Q3 FY2025 model estimate and actual (context for a past quarter). The street range is the comparator. The nearest thing to an answer-shaped number is the Fit sheet intercept 0.77 / slope 0.737 / RMSE 1.3 pp, which is a fitted relation the prompt's "range" and "back-test" asks would be reconstructed from. Reads as context from a prior analyst, but it is a stated model; see Q6.

**5. Filed sentences that fix a graded figure's computation or population, literal reading.**
- xlsx A6: "Kestrel spend per open panel card, merchant ids M0412, M0413 and M2290 (from 2 June 2024) as delivered, issuers in the panel in both quarters, weekly averages." Literal reading: sum spend over those three merchant ids (M2290 only from the acquisition date), divide by open panel cards, restrict to issuers present in both the current and prior-year quarter, average by week. Note it sets population (issuer constancy), merchant set and the "as delivered" vintage choice (use delivery as shipped, not restated).
- xlsx A7: "Reported growth: net sales per week, Fernhollow taken out unless in both quarters." Literal reading: convert reported net sales to per-week (handles the 14-week quarter) and exclude Fernhollow from quarters where it is not in both years.
- xlsx A8: "Fit: least squares, fiscal 2022 Q1 to fiscal 2025 Q2. Back-test: from the seventh quarter, each fitted on the quarters before it." Literal reading: OLS of reported growth on card growth over that window, expanding-window back-test starting at the seventh quarter. This pins the method and the back-test for the prompt's "how that range would have held in each past quarter".
- 10-K: "Fiscal 2023 was the 53 weeks ended February 3, 2024; its fourth quarter had 14 weeks." Literal reading: Q4 FY2023 is 14 weeks and Q4 FY2024 compares with it.
- 10-K: licensee shop-in-shops and Brindle Cafe sales "are not our net sales". Literal reading: exclude those descriptors (Brindle Cafe, Hollister shop-in-shop) from the company's spend.
- Releases: "the thirteen weeks ended ..." plus 14-week labels in the FY2023 Q4 release.

**6. The one thing that would make most of it routine.** The Larkhill xlsx. Its Fit and Q3 call sheets give the whole prior method end to end: per-card spend growth against comparable reported growth, the merchant set, the issuer-constancy rule, the Fernhollow exclusion, per-week normalisation, the OLS and the back-test design, plus a worked prior quarter and a back-test RMSE. Once read, the point estimate, the back-test, and the range are mostly execution of a filed recipe (a "follow the stated procedure" risk). Its stated numbers (intercept 0.77, slope 0.737, RMSE 1.3) also pre-answer the width of the range. Likely fix: if the intent is that the solver builds this chain, shorten A6:A8 to labels without the rule detail, or keep as is only if the design note accepts the model being the baseline the solver must test and improve. Even so, the workbook does not by itself resolve the later steps in the prompt (step-by-step worth in growth points, the call), which still turn on analysis.

Per prompt part:
- Quarter net sales with an 80 per cent range: analysis, but the xlsx note makes the base method follow-a-recipe; the data-semantics sub-points (merchant ids, descriptor variants, panel composition, delivery vintages) are partly handed over by A6 and the 10-K.
- How the range would have held in past quarters: analysis (back-test), with the design given in A8.
- Worth of each step from card data to net sales in growth points: analysis (decomposition), with the Fernhollow and week-count facts supplied by documents.
- The call: rule application of a stated convention against the street figure.
Reading definitions correctly (which merchant ids, which descriptors are licensee, which weeks) carries part of the weight; nothing in the pack looks like a deliberately planted defect beyond ordinary export mess.

**Sweep flags.**
- Nineteen bmh_8k_ex99-1_<date>.txt files: harmless. All 19 are standard earnings releases (EX-99.1, release text, income statement, brand split, balance sheet), the company's own record. None describes the data, the panel, or the cards. Greps for outlook, guidance, expect, anticipate found nothing beyond the boilerplate forward-looking statement.
- Per-share figures coinciding with numbers elsewhere: harmless. Per-share lines (for example Q4 FY2024 diluted 3.02 vs 2.40; Q3 FY2025 2.58 vs 2.39) are historical results and none reads as an answer to the Q4 FY2025 question. There is no Q4 FY2025 release (the latest is 2025-12-10).
- Fourth-quarter releases sharing words with a call sentence: harmless. They state completed Q4 results for earlier years only ("Net sales for the fourth quarter were ... compared with ..."); none says anything about the coming quarter or about fiscal 2025 Q4.
- PDF of 10-K excerpts: harmless on analytical moves (one page, a LibreOffice Writer export titled "research desk copy"); it names no method, only facts: 52/53-week fiscal calendar, Fernhollow acquisition on 2 June 2024, licensee exclusion, net sales by region/brand. It does point at which merchants count and the 14-week quarter, as in Q5, but states them as company facts. One minor note: it carries the header "Larkhill Partners | Research | Internal" and a page footer, consistent with the xlsx.

**Realism and plants.** The data looks like real exports, not tidy. The weekly panel (about 163,000 rows) has issuer, region and card-open-year cuts, merchant name variants for the same id ("BRINDLE & MOSS", "BRINDLE AND MOSS", "Brindle & Moss"; "BRINDLEMOSS.COM", "BRINDLEMOSS COM", "brindlemoss.com"), and a distractor merchant stream within the panel file is not obvious. The delivery-history file records vintages by delivery date. The descriptor file lists store, outlet, cafe, PayPal and Fernhollow descriptors. The app downloads, web visits and the second-tier files are plausible adjacent signals. Nothing is labelled as a distractor, trap or hint. The only things that read as built-in are the 10-K and Fit-sheet sentences above, which are filed as an analyst's notes and a company disclosure respectively rather than as a defect. The street CSV has a "prior_q4_fy2025_net_sales_usd_m" column next to the current estimate (a revision history), which is natural broker data.

### Main thread's rulings (second hardening, 2026-11-12)

- The desk model's Fit sheet notes (A6 to A8): fix. They describe the incumbent's own method (spend per open card on the
  issuers in both quarters, the brand ids as delivered, a regression with its back-test), which is one of the hurried
  routes and lands long; still, a sentence that describes process is out of the pack at the author's direction, so the
  three notes are removed and the workbook keeps its series, coefficients and third-quarter line under field labels only.
- The 10-K's licensed operations, Fernhollow's consolidation date and the 53-week year: harmless. They are the company's
  own disclosures of its population and calendar (Layer 1, earned by the careful column at R1), and none names a step of
  the three deep results.
- The nineteen releases, their per-share lines and the fourth-quarter releases' wording: harmless, as the reader found:
  the company's own historical records, nothing on the coming quarter.
- The prompt's call rule and its opening reason: harmless (the decision convention and the form of the answer).
