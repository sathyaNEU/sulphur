## Tags

**Domain:** Banking, Credit & Financial Risk (expected credit loss provisioning).  
**Analytical objective:** Opportunity Sizing & Decision Support.

## Final Recommendation

**The business support unit should take on Kinloch Engineering and Matai Valley Foods, keeping NZ$3,350,000 of 2027 write-off off Ruahine's book with NZ$5,800,000 of the NZ$6,000,000 envelope.** A package at Matai also keeps out of default the Ruahine borrowers that take most of their receipts from it. Not Kinloch Engineering and Ridgeway Precast, which lead on the two borrowers' own expected write-off but leave Matai's dependants exposed. Not Matai Valley Foods and Ridgeway Precast, the next-best pair inside the envelope, which gives up Kinloch's NZ$1,600,000 for Ridgeway's NZ$1,450,000.

## Supplementary Questions

### bsu_intake_2027.xlsx

1. The first sheet opens with the choice and its total: take on Kinloch Engineering and Matai Valley Foods; 2027 write-off kept off the book NZ$3,350,000. The eight watch-list packages it was chosen from sit below, largest first.
2. For each borrower taken on, the intake to fall back on were it to turn its package down, and the 2027 write-off that intake keeps off, New Zealand dollars to the nearest 50,000:
   - Kinloch Engineering turns its package down: Matai Valley Foods and Ridgeway Precast, NZ$3,200,000
   - Matai Valley Foods turns its package down: Kinloch Engineering and Ridgeway Precast, NZ$3,050,000
3. A second sheet with one row per envelope, giving the intake and the 2027 write-off it keeps off:
   - NZ$4,500,000: Brightwater Motor Group and Matai Valley Foods, NZ$2,200,000
   - NZ$5,000,000: Matai Valley Foods and Selwyn Joinery, NZ$2,450,000
   - NZ$5,500,000: Matai Valley Foods and Ridgeway Precast, NZ$3,200,000
   - NZ$6,000,000: Kinloch Engineering and Matai Valley Foods, NZ$3,350,000
   - NZ$6,500,000: Matai Valley Foods, Northgate Print and Ridgeway Precast, NZ$3,450,000

### bsu_intake_2027.docx

4. A note to the credit committee giving the recommendation and its reasoning: Matai Valley Foods' own expected write-off of NZ$817,000 against NZ$1,750,000 once its dependants are counted, the record's comparison behind that figure, and the fall-back intakes.

## Critical Components

1. A package at Matai Valley Foods also keeps out of default the **8** Ruahine borrowers taking most of their 2026 receipts from it, and one at Ridgeway Precast the **1** taking most of its receipts from Ridgeway; no other watch-list borrower has such a borrower
2. That protection is measured against borrowers just as dependent on a payer that kept trading: borrowers taking 30 per cent or more of their receipts from a payer that defaulted in 2022 to 2025 defaulted within twelve months **13** times in **31**, against **5** times in **211** borrower-years whose such payer was neither in default nor defaulting
3. Priced that way, Matai Valley Foods' package keeps **NZ$1,750,000** off the book, more than twice its own expected write-off of **NZ$817,000**

## Step-by-Step

1. Summed twelve-month PD times LGD times EAD over each watch-list borrower's facilities in ifrs9_facility_run_2026-12-31.csv, borrowers and proposed lines from watch_list_2027-01.pdf: Kinloch Engineering NZ$1,593,000, Ridgeway Precast NZ$1,422,000 and Matai Valley Foods NZ$817,000 of their own. Filling the envelope on these figures alone takes Kinloch Engineering and Ridgeway Precast for NZ$3,000,000, the reasonable analysis this answer rejects.
2. Built each customer's 2026 receipts in business_account_transactions_2021-2026.csv, own-account transfers and Ruahine lending left out and on-us counterparties resolved through customer_master_2026-12.xlsx and account_number_crosswalk_2023.csv: 8 borrowers take most of their receipts from Matai Valley Foods and 1 from Ridgeway Precast.
3. Dated each default by its first trigger in default_register_2021-2026.csv, with cures from default_cures_2021-2026.csv, per the definition in ifrs9_pd_model_validation_2025.pdf: 13 of 31 borrowers that had taken 30 per cent or more of their receipts in the previous twelve months from a payer that defaulted in 2022 to 2025, and were performing at its first trigger, defaulted within twelve months of it.
4. Measured that against borrowers just as dependent on a payer that kept trading: 5 of 211 borrower-years from 2022 to 2025 in which a borrower on ifrs9_facility_run_2024-12-31.csv, ifrs9_facility_run_2026-12-31.csv or the default register, performing at the start of the year and with receipts in its first quarter, had taken 30 per cent or more of the previous calendar year's receipts (own-account transfers and Ruahine lending left out) from one Ruahine customer neither in default at the start of the year nor defaulting during it, and defaulted in the year (any share from 10 to 45 per cent selects the same borrowers). Borrowers that took a smaller share from a failing payer are no control, because that default reached them too.
5. Added to each watch-list borrower its PD times 0.3957 (13 of 31 less 5 of 211) times each dependant's LGD times EAD and ranked the eight: Matai Valley Foods NZ$1,750,000, Kinloch Engineering NZ$1,600,000, Ridgeway Precast NZ$1,450,000 with its one dependant, the rest their own figures.
6. Chose, under section 3 of bsu_terms_of_reference_2027.pdf (a NZ$6,000,000 envelope, whole packages), the proposed lines with the largest total: Kinloch Engineering and Matai Valley Foods, NZ$3,350,000, ahead of Matai Valley Foods and Ridgeway Precast at NZ$3,200,000.
7. Solved the same choice without each borrower taken on (Kinloch Engineering out: Matai Valley Foods and Ridgeway Precast, NZ$3,200,000; Matai Valley Foods out: Kinloch Engineering and Ridgeway Precast, NZ$3,050,000) and at each envelope from NZ$4,500,000 to NZ$6,500,000 (NZ$2,200,000; NZ$2,450,000; NZ$3,200,000; NZ$3,350,000; NZ$3,450,000), Matai in every intake.

No other conclusion survives. Ranking on the borrowers' own expected write-off, twelve-month or lifetime, or adding the dependants' own IFRS 9 expected loss, keeps Ridgeway, because the IFRS 9 model scores each borrower on its own accounts and the trade dependence sits only in the payments ledger; an assumed rise, or one pooled over every payee of a failing payer whatever its share, keeps Ridgeway too. Measuring the rise against the less dependent payees of the same failing payers, or against the book's default rate, keeps the choice but understates the rise, Matai's figure and every intake that holds Matai, since the payer's default reached those borrowers too. Any receipts threshold from 10 to 45 per cent, a 9- to 18-month follow-up, and a baseline from payers that never defaulted or from the dependants' own PDs file the same figures.
