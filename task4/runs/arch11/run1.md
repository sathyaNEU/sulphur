# task4 architecture 11, platform run (pasted by the author, 2026-11-11)

Architecture 11 (Saarnela fulfilment centre's 2027 peak plan, target.zip 2a65f595f7577ba4). One run's full text as the
author pasted it; the second run and the rubric were not supplied. The author's verdict: not stumped.

Against the golden (submission.md, figures.json):
- the call: evening shift weeks 47 to 50 in P1 and P2, week 46 on day shifts: landed exactly;
- agency hours 992, 1,720, 1,736, 1,664, 1,632 (7,744) against 760, 1,910, 1,930, 1,760, 2,030 (8,390);
- the pooled year-ahead overstatement 9.97 per cent (golden R2 10.0, landed); the 2027 expected overstatement read
  as the pooled rate, never conditioned on the budget's own planned growth (golden R5 3.7 per cent: the one judgment
  the run missed; its held-out WAPE improvement from 21.88 to 10.11 per cent confirmed the pooled correction);
- the Huippu Sport difference +0.129 minutes a line at comparable zone and density (golden R4 0.13: landed);
- aisle congestion modelled as a logged picker-density term with the January 2024 aisle expansion (golden R3: landed);
- the 53-week calendar re-keyed (Black Friday 26 November 2027 in ISO week 47; golden R6: landed);
- Saturday carryover, the 6 December closure, sickness by zone, 10,000-scenario ranges and a frozen-model back-test,
  all unprompted.
Named and waved through: "Kotikaari's forecast-error factors transfer to Huippu"; "the pilot process allowance transfers
across classes and zones". Route: REDESIGN (architecture 12, a new world and decision form).

---

Reviewed 134 resources
· 50m
Recommendation. Run evening shifts in P1 and P2 in weeks 47-50, not week 46; book 992, 1,720, 1,736, 1,664 and 1,632 agency picker hours for weeks 46-50, respectively.

The critical week-48 constraint is Saturday carryover: 5,791 P1 lines and 6,896 P2 lines remain after Black Friday's Saturday picking. Including that backlog, week-48 workloads exceed both zones' day-only capacities.

Final answers. The workbook is Saarnela_Peak_2027.xlsx; the one-page memo is Saarnela_Peak_2027_Memo.pdf.

Forecasts below are paid picker hours, with the 80% planning range in parentheses. Agency hours are additional to sickness-adjusted own staff.

Week 46, commencing 15 November: P1 875 h (764-1,192); P2 797 h (663-1,096); B1 495 h (420-560). Book 312 / 360 / 320 agency hours for P1/P2/B1, totaling 992 h. Evening shift: No in both small-parts zones.
Week 47, commencing 22 November: P1 1,192 h (832-1,282); P2 1,102 h (751-1,189); B1 609 h (518-689). Book 624 / 664 / 432 agency hours, totaling 1,720 h. Evening shift: Yes in both zones.
Week 48, commencing 29 November: P1 1,249 h (867-1,388); P2 1,163 h (808-1,287); B1 499 h (425-564). Book 688 / 728 / 320 agency hours, totaling 1,736 h. Evening shift: Yes in both zones.
Week 49, commencing 6 December: P1 1,096 h (819-1,204); P2 1,014 h (912-1,109); B1 504 h (429-570). Book 640 / 664 / 360 agency hours, totaling 1,664 h. Evening shift: Yes in both zones.
Week 50, commencing 13 December: P1 1,192 h (799-1,302); P2 1,105 h (726-1,204); B1 516 h (440-583). Book 624 / 672 / 336 agency hours, totaling 1,632 h. Evening shift: Yes in both zones.
These figures appear in the workbook's Decision, Zone Plan and Agency sheets and the memo's staffing table. Total agency booking is 7,744 hours, rounded upward separately for day and evening work to whole 8-hour shifts.

Kotikaari forecast overstatement: Year-ahead forecasts overstated placed peak order lines by 9.97% across 2022-2025: 1,731,838 forecast lines versus 1,574,868 actual lines. The figures are 10.57% for small parts and 5.68% for bulky, using actual lines as the denominator. See Bias Summary, Bias Detail and the memo's "Forecast bias and Huippu picking time" section.

Huippu picking-time difference: At the forecast peak mix, Huippu averages 1.371 TASK minutes per line, versus Kotikaari's 1.320, a difference of +0.051 minutes per line. Holding zone and density comparable gives +0.129 minutes; the zone-specific differences are P1 +0.283, P2 +0.030 and B1 +0.025 minutes. These are modeled task-time estimates, not paid-hour rates. See Picking Time, Task Model and the same memo section.

Step-by-step process.

Reviewed all archive members. Demand inputs were kotikaari_budget_2027.xlsx, kotikaari_forecast_archive_2021-10_2026-10.csv, wms_order_import_kotikaari_2022-01_2026-10.csv and huippu_orders_daily_2024-01_2026-10.csv. Picking inputs were the Huippu article-line, slotting, pilot-review and confirmation files, plus the WMS item master and zone-hours file. Staffing inputs were both payroll files, the own-picker roster, labour standard and agency agreement. The draft staffing workbook was used only as a comparator. Returns and packing-bench files were reviewed but excluded from picking demand and hours. The complete inventory is in Source Audit.

Cleaned and reconciled the records. Removed 81 exact WMS repeats, leaving 33,996 rows. Excluded 715 zero-line/zero-task rows only from task-rate fitting. Removed 644 payroll reruns, leaving 26,761 current payroll records; combined with 16,583 legacy records, the payroll control total is 43,344. Legacy payroll required semicolon parsing, comma-decimal conversion, Finnish-date parsing and cost-centre translation. Packing records remained in controls but not zone picker hours.

Audited the pilot and assortment joins. Removed 136 confirmation retransmissions, leaving 26,535 unique tasks, which reconcile to the pilot WMS counts. All article-month records joined to the item master and future slotting. Historical peak weighting used 15,713 article-month records, containing 295,582 lines and 355,445 units. Future slotting resolved 3,770 missing current pick-zone values; those articles were not discarded. Of 4,050 intended articles, 4,041 had historical peak weight.

Measured comparable forecast error. Selected 40 completed peak year/week/product-line pairs, using the latest pre-year annual budget and actual lines placed in those same weeks. Excluded 1,560 rolling-forecast rows, superseded 52 annual-budget rows, and did not use incomplete future peaks. Applied separate small-parts and bulky actual-to-budget factors rather than subtracting an overstatement percentage directly.

Corrected event and release timing. Black Friday falls on 26 November 2027, ISO week 47, whereas the supplied budget uses 2025's week-48 phasing. Swapped the relevant budget weeks and daily profiles, preserving total demand. Expanded the forecast into 224 daily owner/product-line records, then moved web orders to the next working pick date. Accounted for the 6 December closure and propagated Saturday backlog into the following week.

Estimated workload-dependent picking time. Fitted task minutes using handling-class mix, extra units and a nonlinear logged-picker-density term, allowing for the January 2024 aisle expansion. The model used 33,281 positive-line observations. This was preferable to a flat historical rate because the combined workload changes both assortment mix and congestion. The pilot's adjusted Huippu process allowance is +0.056 minutes per line, with a sampling interval of +0.031 to +0.080 minutes; its transfer beyond class-A P2 is explicitly qualified.

Built a release-constrained staffing schedule. Available own pickers are 15 in P1, 12 in P2 and 5 in B1, after excluding the employee on long leave and including the planned starters. Applied peak-2025 sickness rates of 4.92%, 7.63% and 8.80%. The daily schedule respects 24 P1 / 22 P2 floor limits, clears weekday work, and carries unavoidable Saturday excess forward. Week 49 has 5 day shifts and 4 evening weekdays, rather than 6 and 5.

Calculated uncertainty and tested sensitivity. Generated 10,000 scenarios combining calendar-aligned historical forecast errors, Huippu transfer risk, task-time variation and logged-availability variation. Each scenario carries backlog between weeks. Reported marginal P10-P90 scheduled hours, not confidence intervals around a mean or additive zone endpoints.

Validated the results. Held-out demand WAPE fell from 21.88% for raw budgets to 12.11% after calendar alignment and 10.11% after held-out bias correction. A frozen pre-2025 task model achieved 2025 WAPE of 1.75% / 1.68% / 1.75% for P1/P2/B1. The final audit reconciled daily and weekly balances, checked floor limits and holiday restrictions, verified workbook formulas and cached results, and confirmed that the one-page memo matches the workbook.

Assumptions and judgment calls.

Promotions follow Black Friday. This supports correcting the inherited 2025 phasing. Retaining the supplied phasing instead produces evenings in weeks 48-50, so this assumption materially affects week 47.
Kotikaari's forecast-error factors transfer to Huippu. The budget states that they share forecasting governance, but there is no equivalent Huippu year-ahead archive. Additional transfer uncertainty is included.
The pilot process allowance transfers across classes and zones. Direct pilot evidence is limited to selected class-A P2 articles and trained pickers. Removing that allowance does not change the recommended evening weeks.
The schedule prioritizes feasible clearance, not minimum theoretical cost. It includes daily release restrictions and Saturday carryover rather than assuming all weekly demand is available at the start of the week.
Agency crews are already inducted. A new arrival uses 2 paid hours of the first shift for induction, requiring productive cover. Rounded booking surplus is held off-floor, not used to exceed zone limits.
The 80% ranges are conditional planning ranges. Their full-launch coverage cannot yet be validated. They include judgmental transport and operating uncertainty, disclosed in Method.
Week 50 is sensitive. With 5% fewer lines, P1 no longer needs its evening shift in weeks 47 and 50; P2 retains all four evening weeks under the daily release profile.
Alternatives rejected.

Day-only operation in week 48: rejected because it omits the 5,791 / 6,896-line Saturday carryover.
Using the supplied weekly phasing unchanged: rejected as the base case because it places the Black Friday peak in the wrong 2027 ISO week; retained as a sensitivity.
Applying the pilot's 0.88 productivity multiplier: rejected because selected fast-article scanner intervals are not comparable with full-assortment WMS task time.
Using a flat 2025 paid-minutes-per-line rate: rejected because it cannot represent changing mix, congestion, release timing and idle booked capacity.
Treating returns or packing activity as picking: rejected because those files describe different workloads and cost centres.
Treating the 80% upper bounds as bookings: rejected because the stated booking plan covers central demand; the ranges describe risk, and late agency additions are not guaranteed.
Files produced.

Saarnela_Peak_2027.xlsx: staffing decisions, agency bookings, daily schedule, backlog reconciliation, forecast bias, picking-time model, source audit, validation and sensitivities.
Saarnela_Peak_2027_Memo.pdf: one-page operating recommendation with the complete weekly staffing table.
Both are saved under /home/agent/workspace. Temporary analysis files were removed.

Packages installed. Installed pandas, NumPy, SciPy, openpyxl, python-docx, PyMuPDF, ReportLab, XlsxWriter and statsmodels, with their dependencies, in a temporary package environment.
