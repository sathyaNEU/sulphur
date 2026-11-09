Recommendation. Order 6 battery-electric tractors for V02, V05, V09, V14, V16 and V18; keep the other 8 shortlisted duties diesel under FES-2. The quoted 540 kWh usable battery, adjusted for 3.8% permanent first-year loss and the required reserve, provides a 440 kWh duty-energy ceiling, rounded; eligibility was tested before rounding.

Final answers. The order and assignments appear in Varnamo_2027_Order_Memo.pdf and the spreadsheet's Duties sheet.

Every shortlisted duty is listed below. Loads are to 0.1 t; energies are round-trip battery draw at the -5 C January design day, rounded to the nearest 10 kWh. These figures appear in the spreadsheet's Duties sheet and the memo's duty table.

V02, Kalmar: 3.9 t; 410 kWh; electric.
V03, Helsingborg: 29.1 t; 450 kWh; diesel.
V05, Angelholm: 7.6 t; 420 kWh; electric.
V07, Linkoping: 32.0 t; 450 kWh; diesel.
V09, Goteborg: 20.9 t; 400 kWh; electric.
V11, Kristianstad: 26.6 t; 450 kWh; diesel.
V14, Karlskrona: 4.7 t; 430 kWh; electric.
V16, Varberg: 9.1 t; 410 kWh; electric.
V18, Alingsas: 5.5 t; 420 kWh; electric.
V21, Malmo: 18.5 t; 470 kWh; diesel.
V24, Oskarshamn: 20.9 t; 470 kWh; diesel.
V27, Trollhattan: 13.6 t; 470 kWh; diesel.
V30, Uddevalla: 13.4 t; 460 kWh; diesel.
V33, Vastervik: 4.0 t; 480 kWh; diesel.
One additional tonne adds 2.0 kWh per 100 loaded km, with a 95% interval of 1.8-2.1 kWh. Permanent first-year usable-battery loss is 3.8%, with a 95% interval of 3.7%-3.8%. Both appear in the memo's "Energy and battery evidence" section and the spreadsheet's Method and Model QA sheets.

The order totals SEK 23,640,000 excluding VAT, at SEK 3,940,000 per tractor. The quotation requires ordering by 11 December 2026 for January-February 2027 delivery. These details appear in both deliverables.

Step-by-step process.

Established the policy and commercial basis. Read fleet_electrification_standard_FES-2.pdf, fleet_plan_2027.xlsx and quotation_bev_tractors_2027.pdf. FES-2 fixes the design temperature, planning-load window, permanent-loss adjustment, 85% energy limit and one tractor per qualifying duty. The shortlist contains 14 duties; the quotation supplies usable capacity, price and delivery terms.

Read the supporting registers and operating files. route_register_2026.xlsx supplied distances, loaded legs, climb and historical duty aliases. fleet_register_2026.xlsx supplied pilot service dates, battery capacity and equipment tares. shipper_register_2026.xlsx supported shipper and full-load-service checks. The telemetry, TMS, weighbridge and temperature CSVs supplied the analytical observations. All files and their uses are documented in Sources.

Prepared the weighbridge departures. Mapped historical VMO-xx codes to current duties and retained the final weighing per duty, date and CMR. This removed 457 superseded weighings from 21,470 rows, leaving 21,013 departures. Two CMR references recurring on different dates were retained. Every recorded tare reconciled to tractor plus trailer register tares. Net payload was calculated as gross minus tare, converted from kilograms to tonnes; no nonpositive net loads or gross weights above 64 t required exclusion.

Calculated the planning loads. For the assessment on 9 November 2026, the required window is 1 November 2025 through 31 October 2026. Its 10,757 raw weighing rows became 10,528 final departures after removing 229 superseded weighings. Excluding 7,238 non-shortlisted departures left 3,290 departures, exactly 235 per shortlisted duty. Planning loads are their arithmetic mean net payloads.

Reconstructed the electric pilot sample. Reduced 2,374 telemetry rows to 2,334 unique vehicle-days by removing 40 repeat uploads. Matched these to TMS by registration and date, then to registered duties. All joins succeeded; 1,167 other TMS records were outside the electric sample. Parsed unlabelled kilograms, spaced kilogram strings and comma-decimal tonnes. Filled 82 missing tractor temperatures with same-date Jonkoping station observations. No required-value gaps or nonpositive modelling inputs remained.

Corrected declaration noise before estimating the payload effect. After final-weighing selection, 258 departures lacked declarations, leaving 20,755 paired declared and weighed loads. Of these, 6,780 belonged to the six pilot shippers; 13,975 belonged to other shippers and were not used for pilot-error calibration. Relative RMS declaration errors were 20.4%-22.1% for five pilot shippers and 4.6% for BMJ. The model therefore corrects measurement-error variance rather than treating declared weights as exact. Calibration, Bridge Audit and Normal Equations preserve the evidence and calculation.

Estimated transferable battery-energy demand. Modelled pilot battery energy per distance using loaded payload exposure, temperature, temperature squared and route climb. The temperature quadratic reduced ordinary-model RMSE from 5.21 to 3.46 kWh/100 km relative to a linear-temperature specification. Applied the corrected model to each shortlisted route at its unrounded planning load and -5 C, including the complete round trip. Duty Audit retains the unrounded forecasts and comparisons.

Separated permanent ageing from reversible cold effects. Inferred daily effective battery capacity from reported energy divided by the SOC fraction consumed. Regressed capacity on service age, temperature and tractor effects. The age effect, relative to the pilot's 520 kWh manufacturer-usable capacity, gives 3.8% permanent first-year loss. Applied that loss to the quoted 540 kWh usable capacity, then applied the FES-2 85% limit.

Checked validation and decision stability. A later-period holdout used 1,890 training vehicle-days and 444 test vehicle-days, assessed as 36 duty-month means. Mean-energy RMSE was 2.05 kWh. All 3,000 bootstrap draws retained the same six assignments. Restricting calibration dates, changing measurement-error variance by 10%, using complete temperature cases and using the within-duty payload estimate also retained the same six. These checks appear in Holdout, Sensitivity and Model QA.

Verified the saved artifacts independently. Reopened the spreadsheet and reconstructed loads, calibration moments, corrected forecasts, battery loss, threshold and decisions using only its saved contents. Confirmed all displayed rounding and all 14 decisions. Reopened and visually checked the PDF, confirming it is one page. Temporary analysis files were removed.

Assumptions and judgment calls.

Final weighbridge net payload is treated as accurate, and each shipper's declaration-error process is assumed transferable between Varnamo and Jonkoping. Calibration-period and variance sensitivities leave the order unchanged.
Energy scales linearly with route distance after accounting for payload, temperature and climb. The new round trips are 266-355 km, compared with 202-241 km for the pilot routes, so this remains a transfer assumption.
The new tractors are assumed to have comparable operating efficiency to the pilot fleet. Manufacturer consumption claims were not substituted for company operating evidence.
Permanent loss is estimated with a linear age effect after controlling temperature. Adding an age-squared term gives 3.7% first-year loss and does not change assignments.
Bootstrap intervals describe conditional mean estimates, not guarantees for individual trips or protection against omitted new-route effects.
The terminal charger bank must be commissioned before service begins. No road charging or sharing one tractor between qualifying duties is assumed.
Alternatives rejected.

Uncorrected declared-weight regression: produces a payload effect of 1.2 kWh/t/100 loaded km and an 8-tractor assignment. It ignores directly observed declaration noise and changes which duties qualify.
Ignoring permanent battery loss: produces a 10-tractor assignment and does not comply with FES-2.
Pallet counts as the primary instrumental variable: BMJ declared tonnes equal 0.54 times pallets in all 389 of its TMS rows, so that instrument inherits declaration error. Direct weighbridge calibration is better supported.
Diesel purchases as electric-energy evidence: fuel_card_statement_varnamo_2025-2026.csv contains 9,357 diesel-purchase records, not battery draw.
Workshop costs as degradation evidence: workshop_log_2025-2026.csv contains 504 service records, but no usable-capacity measurements. It was inspected for relevant interventions, not used to estimate loss.
Historical average January weather, installed capacity or warranty capacity: none is the FES-2 planning quantity. The temperature file was used only to fill pilot temperature gaps.
Evidence warranting caution includes changing GDR declaration-error variance and the longer target routes. The documented calibration sensitivities preserve the recommendation, but initial winter monitoring remains important.
Files produced.

Varnamo_2027_Duty_Assessment.xlsx: duty decisions plus methods, unrounded calculations, calibration, validation, source inventory and supporting audit records across 12 sheets.
Varnamo_2027_Order_Memo.pdf: one-page management memo containing the order, commercial timing, complete duty table and principal evidence.
Packages installed. Installed pandas, numpy, scipy, statsmodels, openpyxl, pymupdf and reportlab, plus their required dependencies, because the active Python environment lacked the required packages.
