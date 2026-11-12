## Tags

**Domain:** Energy Systems & Utilities, grid operations (distribution losses and the feeder energy balance).
**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).

## Final Recommendation

**Sweep CHL-2, APT-4, NTH-4 and CHL-3 in 2027:** they carried 1,310, 1,122, 700 and 699 MWh of non-technical loss in the twelve months to September 2026, and the next feeder, NTH-3, carried 503. Reject the four that the residual gives on the old loss study's percentages, today's GIS and the storm gap carried at the feeder's average (APT-4, APT-3, CHL-2 and NTH-3): APT-3's excess is its own network losses (1,787 MWh at its 2026 loads, not the study's 833), and NTH-3 looks high only while the lateral it passed to NTH-4 on April 21 is counted on NTH-4 for the whole year.

## Supplementary Questions

### revenue_protection_2027_memo.pdf

1. One page to the utility director: the four feeders to sweep in 2027 with their non-technical loss in the twelve months to September 2026 (CHL-2 1,310, APT-4 1,122, NTH-4 700 and CHL-3 699 MWh, each within the band in answer 3), the next feeder (NTH-3, 503 MWh), why APT-3 and NTH-3 are not on the list, the line loss rise and its split, the 2027 technical losses, and a horizontal bar chart of all fourteen feeders' non-technical loss with the four in blue.

### dpl_feeder_energy_balance_2023-10_2026-09.xlsx

2. Monthly balance: 504 rows, one per feeder and month from October 2023 to September 2026, columns month, feeder, customers at month end, energy in at the breaker, received from customers' generation, delivered through customers' meters, large power meters, city street and area lights, technical losses and non-technical loss (MWh). NTH-4 served 374 customers at the end of March 2026 and 441 at the end of May 2026 (each within 3). CHL-3's energy in is 1,340.5 MWh for January 2026 (within 3 per cent) and 12,232.6 MWh for the twelve months to September 2026 (within 0.6 per cent); the fourteen feeders' is 248,001.4 MWh (within 0.12 per cent).
3. Twelve months to September 2026, by feeder: NTH-4's customers' meters recorded 9,377.7 MWh and NTH-3's 6,707.5 (each within 1.5 per cent); the city's lights used 874.1 MWh (within 4 per cent) against 1,145.7 billed at deemed kWh; technical losses 1,786.6 MWh on APT-3, 1,189.0 on APT-4 (each within 7 per cent) and 13,002.6 on the fourteen feeders (within 4 per cent); non-technical loss CHL-2 1,310.4 MWh (1,192.5 to 1,428.3); APT-4 1,121.9 MWh (1,020.9 to 1,222.9); NTH-4 700.3 MWh (625.3 to 775.3); CHL-3 698.9 MWh (623.9 to 773.9); NTH-3 502.7 MWh (427.7 to 577.7); APT-3 456.6 MWh (381.6 to 531.6).
4. Line loss bridge sheet: line loss 7.74 per cent in the twelve months to September 2024 and 8.24 per cent in the twelve months to September 2026 (each within 0.05); of the 0.50 point rise, technical losses +0.44 points, non-technical losses +0.30 points and everything else -0.24 points (each within 0.10).
5. 2027 sheet, the peak hourly demand each approved 2027 connection adds: LL-2026-433 521.6 kW; LL-2026-722 931.4 kW; LL-2026-964 541.2 kW (each within 5 per cent).
6. 2027 sheet, each feeder's 2027 technical losses: APT-4 1,720.9 MWh and APT-3 1,694.1 MWh (each within 7 per cent), 13,455.3 MWh on the fourteen feeders (within 3 per cent).

## Critical Components

1. Technical losses at the loads' 2026 positions: APT-3 **1,786.6 MWh** and the fourteen feeders **13,002.6 MWh** (5.24 per cent of their energy in), where the 2019 study's percentages give 832.9 and 10,787.0.
2. The switching log replayed on the network: NTH-4 served **374** customers at the end of March 2026 and **441** at the end of May, after the April 21 transfer; today's GIS puts 440 on it in March.
3. CHL-3's energy in rebuilt for the ice storm's missing hours from the Cherry Hill delivery point: **1,340.5 MWh** in January 2026 and **12,232.6 MWh** for the twelve months.
4. The rise in line loss from 7.74 to 8.24 per cent: technical losses **+0.44 points**, non-technical **+0.30 points**, everything else **-0.24 points**.

## Step-by-Step

1. Put the delivery point meters (hour ending, standard time) and the feeder breakers' historian (hour beginning, local clock, the November hour twice) on one hour grid, with the stuck APT-2 transducer of August 2025 treated as missing; the breakers then tie to each substation's purchases less its transformer losses and station service wherever all of them reported.
2. Rebuilt every missing breaker hour from its substation's balance: CHL-3's telemetry was down from January 23 to February 3, 2026, while it carried CHL-2's customers through the emergency tie, so January's energy in is 1,340.5 MWh; carrying the gap at CHL-3's own average for the hour gives 1,033.6, and the twelve months 12,232.6 against 11,866.2.
3. Replayed every switching order on the GIS network (the old OMS names through the July 2024 crosswalk and the pole tags), so each node has its feeder hour by hour: the April 21, 2026 transfer leaves NTH-4 with 374 customers in March and 441 in May, and NTH-4's meters recorded 9,377.7 MWh in the twelve months where today's GIS gives 9,871.9 (494.2 MWh of NTH-3's use).
4. Spread each read period's kWh over its days by the substation's daily energy, an estimated read folded into the actual read that trues it up; the lights at their lamp's input watts and each month's burning hours used 874.1 MWh against 1,145.7 billed at deemed kWh.
5. Technical losses: each month's metered load at each node of the tree that served it gives the feeder an equivalent resistance from the GIS segments at the study's conventions (single-phase taps at six times, secondary at 0.7 per cent of metered energy), times each hour's breaker current squared, with transformer core and copper losses from the register by vintage: APT-3 1,786.6 MWh, where the study's 4.78 per cent of its 2026 energy gives 832.9, because the cold store and a grow now sit at the end of its main.
6. Non-technical loss is energy in plus customers' exports, less their meters, the large power meters, the lights and technical losses: CHL-2 1,310, APT-4 1,122, NTH-4 700, CHL-3 699, NTH-3 503, APT-3 457; the careful but hurried route (today's GIS, the gap at the average, the study's percentages) files APT-4 1,574, APT-3 1,403, CHL-2 1,335, NTH-3 977 and sweeps APT-4, APT-3, CHL-2, NTH-3.
7. The bridge: purchases at the delivery points and sales on bills issued in each window give 7.74 and 8.24 per cent, split into the substations, technical losses, non-technical losses, the lights and billing timing; technical losses take +0.44 points of the rise, where holding them at the study's percentage leaves +0.56 to theft.
8. 2027: the connected grows' peak hourly demand from the interval meters is 0.745 of the load they applied for and the cold store's 0.660, so the three approved connections add 521.6, 931.4 and 541.2 kW; their loads at the existing grows' hourly shape on today's network, with APT-3's main reconductored from March 15, 2027, give APT-4 1,720.9 MWh, APT-3 1,694.1 MWh and 13,455.3 MWh on the fourteen feeders (the applied loads give 2,433.8 on APT-4).

No other four survives. The same four come out with load placed by each node's twelve-month energy or with each read period spread evenly over its days, and under conductor resistance at 25 C, transformer losses 10 per cent either way, burning hours 5 per cent lower and substation losses 20 per cent higher. Each shortcut lands on a different four: the study's percentages put APT-3 in for CHL-3, today's GIS puts NTH-3 in for NTH-4, and the storm gap carried at the average puts NTH-3 in for CHL-3; placing load by transformer rating is ruled out because every transformer's customers are metered.
