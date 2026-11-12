## Tags

**Domain:** Energy Systems & Utilities, energy efficiency and demand response evaluation.
**Analytical objective:** Experiment & Causal Analysis.

## Final Recommendation

**Renew Corvane, Ardena and Kitebrook for summer 2027; do not renew Lumivale, Ondera or Pinecrest Home.** Kitebrook's 2027 devices take 0.749 kW each off our load in the 4CP intervals against the 0.602 kW its price needs, Lumivale's 0.306 against 0.431 and Pinecrest Home's 0.306 against 0.380. This rejects reading the test events' own reduction at the 4CP intervals, which renews Lumivale (0.552 kW) and Pinecrest Home (0.454 kW) and drops Kitebrook (0.505 kW): the 4CP days come late in heat waves, when members leave events; Pinecrest Home's 2027 fleet is mostly retail-rebate devices; and Kitebrook's homes are larger and older than the research sample's.

## Supplementary Questions

### provider_renewals_2027_workbook.xlsx

1. Sheet 'providers', each provider's kW per device enrolled on 1 July 2027 taken off the co-op's load in the 4CP intervals of a summer like 2024 to 2026, each within the kW given beside it (the spread of the defensible methods): Corvane 0.630 (within 0.056), Lumivale 0.306 (within 0.020), Ardena 1.015 (within 0.061), Ondera -0.125 (within 0.072), Kitebrook 0.749 (within 0.045), Pinecrest Home 0.306 (within 0.020). Sheet '4CP intervals' gives each of the 12 intervals, the 18 September 2025 interval at nothing for every provider (no alert was called).
2. Sheets 'providers' and '2027 fleets', each provider's devices enrolled on 1 July 2027 and what its quote would cost (each within 3 per cent): Corvane 2,127 devices, $61,683; Lumivale 1,984 devices, $46,822; Ardena 1,268 devices, $51,988; Ondera 1,253 devices, $32,578; Kitebrook 1,511 devices, $49,863; Pinecrest Home 2,760 devices, $57,408.
3. Sheet 'providers', the renewed providers (Corvane, Ardena, Kitebrook) in all: 3.76 MW off the co-op's 4CP load, saving $206,000 of transmission cost, $42,500 net of the $163,534 their quotes cost (each within 8 per cent).

### provider_renewals_2027_memo.docx

4. A memo of about a page for the board: the call first, a table of each provider's kW per 2027 device against the kW its price needs, its devices, its quote's cost and the verdict, a chart of the six against their lines, and short paragraphs on why the test events overstate Lumivale and Pinecrest Home and understate Kitebrook, and on Ondera's window.

## Critical Components

1. On the 4CP days **33%** of Lumivale's enrolled devices were still in its event at the middle of the 4CP interval (between 31% at its end and 36% at its start; the band runs 2 points beyond both), against **64%** of its called devices on the test events at 17:30 (within 3 points).
2. Pinecrest Home's 2027 fleet is **65%** retail-rebate devices and keeps **59%** of its devices in the event at the 4CP intervals, against **85%** of today's fleet on the 4CP days (each within 3 points).
3. Kitebrook's 2027 fleet sheds **1.54** times what its research-sample devices shed, by the homes' cooling slopes from living area and year built (within 0.06).
4. Ondera's event ends at 17:00, before **10** of the twelve 4CP intervals, so its devices add load there: **-0.125** kW per device.

## Step-by-Step

1. Put the six providers' reports on one footing (`corvane_event_report_2024_2026.csv` and `kitebrook_events_2024_2026.csv` on UTC, the rest local; Corvane, Lumivale and Ardena list unreached devices, Ondera, Kitebrook and Pinecrest Home leave them out) and keyed each row to its programme id through `peak_partners_roster_2026-10-30.csv`, swapped thermostats included; mapped the research sample's meters through `member_accounts_2026.csv`, exchanges included.
2. Measured each provider's reduction on the 24 randomised test events (`mv_event_assignments_2024_2026.csv`, `ami_15min_reads_peak_partners_2024_2026.csv`): held-back half against called half, 15 minutes at a time, each home's own 13:00 to 14:30 load that day as the covariate.
3. Split the reduction into the shed of a device still in the event (a straight line in the interval's temperature, `weather_kcdr_hourly_2024_2026.csv`) and the share still in it, every enrolled device in the denominator.
4. Read the share on the 4CP days themselves (`ercot_4cp_intervals_2016_2026.csv` against `peak_partners_event_log_2024_2026.xlsx`): each 4CP day is the third or later alert day of a heat wave, and Lumivale keeps 33% at the 4CP interval against 64% on the test events. The hurried reading takes the test events' reduction straight to the 4CP intervals.
5. Carried each fleet to 1 July 2027 (the devices enrolled now, each at its channel's leaving rate since 2021, and the quotes' new enrolments (`provider_quotes_summer_2027.xlsx`) like the provider's recent enrolments through the same channel); the share in the event modelled device by device on the 4CP days (the day, the channel, the years enrolled) and taken for the 2027 fleet. Pinecrest Home's fleet becomes 65% retail and keeps 59% in the event.
6. Carried the shed to each fleet's homes: each research-sample home's cooling slope off its quiet days, predicted for every home from living area and year built in `calder_cad_residential_2026.csv` matched by address (county roads and FM roads in two forms); Kitebrook's fleet sheds 1.54 times its sample devices'.
7. Read each provider at each 4CP interval's place in its window (Ondera's after its 17:00 end), 18 September 2025 at nothing, and averaged the twelve: Corvane 0.630, Lumivale 0.306, Ardena 1.015, Ondera -0.125, Kitebrook 0.749, Pinecrest Home 0.306.
8. Set each against the kW its quoted price needs at $54.80 per kW (`board_policy_412_demand_response_providers.pdf`, `transmission_charge_notice_2027.pdf`): Corvane, Ardena, Kitebrook clear it; Lumivale, Ondera, Pinecrest Home do not.
9. The renewed providers' 4,906 devices take 3.76 MW off the 4CP load and save $206,000, $42,500 net of their quotes.

No other conclusion survives. Reading the test events' reduction at the 4CP intervals renews Lumivale and Pinecrest Home and drops Kitebrook, but the 4CP days' own reports show Lumivale's members leaving its long, deep event late in a heat wave, the quotes and the roster put Pinecrest Home's 2027 fleet in the retail channel that is often offline and leaves events, and the appraisal roll puts Kitebrook's fleet in homes that shed far more than the research sample's. Each correction alone moves its own provider across its line, and every defensible variant of each (a linear home model, one leaving rate for every channel, the test halves compared without the pre-event load) keeps the same three renewed.
