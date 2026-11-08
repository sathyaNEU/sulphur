## Tags

**Domain:** Other, Urban & Regional Science (supply chain and logistics: last-mile route economics of a retailer's own van fleet).  
**Task type:** forecasting (demand, load and capacity prediction).  
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Hand Mulranny, Achill, Bangor Erris, Belmullet, Louisburgh and Ballycastle to Owenduff from January 2027 and keep Leenane, Letterfrack, Clifden, Cong and Charlestown: the hand-over saves about EUR 50,000 net in 2027.** Pricing each district at the van time its own stops take hands Leenane and Letterfrack over too and claims EUR 20,000, but the Connemara van drives through both on its way to Clifden, which stays, so they save only their own stops; and pricing districts one at a time keeps Mulranny and Bangor Erris, which become the end of the Achill and Erris runs once Achill and Belmullet go.

## Supplementary Questions

### district_handover_2027.xlsx

1. A Districts sheet with one row per district in Owenduff's offer, in the offer's order, giving the code, the district, its run, its 2027 plan parcels, Owenduff's 2027 charge and the decision: Mulranny, Achill, Bangor Erris, Belmullet, Louisburgh and Ballycastle go; Leenane, Letterfrack, Clifden, Cong and Charlestown stay.
2. A Runs sheet with one row per run that serves an offered district, giving the districts it hands over, its 2027 van-hours as things stand and after the hand-over, and the van-hours saved, to the nearest 50: R03 Westport and Louisburgh 300; R04 Newport and Achill 650; R05 Connemara 0; R06 Ballinrobe and Cong 0; R07 Crossmolina and Erris 600; R08 Ballina and the north coast 200; R09 East Mayo 0.
3. The sheet ends on the year's net saving after Owenduff's charges: EUR 50,000 (to the nearest EUR 5,000).

### handover_2027.png

4. Paired bars for each of those runs, 2027 van-hours as things stand beside 2027 after the hand-over, each bar labelled with its value to the nearest 50 (R03 1,300 to 1,000; R04 1,550 to 900; R05 1,700 to 1,700; R06 1,200 to 1,200; R07 1,600 to 1,000; R08 1,550 to 1,350; R09 1,600 to 1,600), with the title stating the districts that go and the net saving of about EUR 50,000.

## Critical Components

1. On the Connemara run, Leenane and Letterfrack together take only **110 van-hours** off 2027, **EUR 6,300** at the van-hour rate against Owenduff's **EUR 12,200**, because the van drives through both to reach Clifden; the whole run beyond Aghagower costs EUR 50,800 against Owenduff's EUR 65,400, so the run keeps all three.
2. Bangor Erris on its own takes **70 van-hours** off the Erris run (EUR 4,100 against Owenduff's EUR 6,300), but with Belmullet gone it is the end of the run, and the two together take **600 van-hours** off it.
3. Mulranny on its own takes **80 van-hours** off the Achill run (EUR 4,500 against Owenduff's EUR 7,800); with Achill gone, Mulranny and Achill together take **650 van-hours** off it.
4. The 2027 van-hours are a forecast of road sections driven on the days a district beyond them has a stop, from the plan's stops month by month; carrying the last twelve months' hours forward in proportion to parcels overstates the year's net saving at **EUR 55,000**, against **EUR 50,000**.

## Step-by-Step

1. Read Owenduff's offer (the offered districts, EUR 12.60 a parcel delivered in 2027, any combination) and NPS-3 section 4 (the saving is the cost at the 2027 all-in rate of the van-hours the hand-over takes off the runs, less Owenduff's charges; the districts handed over are those whose hand-over lowers the year's cost most); took EUR 58.00 a van-hour from the 2027 rate card and the delivery days from the 2027 calendar.
2. Cleaned the stop log: dropped the stop rows a handheld sent again when it re-synced (same stop and times, later sync), mapped CBN and CBS back to Castlebar town through the register's code changes, kept failed attempts and collections as stops, and timed each drive from the previous stop's departure, the break or depot out in the van run log.
3. Read each run's road order from the stop sequences: every run sweeps its districts outward and drives back from the farthest one it served that day.
4. The field's cost-to-serve build, each district's drive in from the stop before, the drives between its stops and its door time over November 2025 to October 2026 carried to 2027 by plan parcels, hands over Mulranny, Achill, Bangor Erris, Belmullet, Louisburgh, Leenane, Letterfrack and Ballycastle and claims EUR 20,000; it prices Leenane at EUR 7,500 and Letterfrack at EUR 10,200 against Owenduff's EUR 5,000 and EUR 7,200.
5. That build charges a district with drive its run makes anyway: on the run-days when Leenane or Letterfrack had no stop the Connemara van still drove the road through them to Clifden, so their saving is the run time without their stops, not the time their stops take.
6. Fitted each run's road sections and district access times by least squares on the observed drives between districts and to and from the depot (2025 and 2026), and each district's door time and drive between its own stops; the fit reproduces the drives on the run-days that skipped a district.
7. Priced districts one at a time on that model: it hands over only Achill, Belmullet, Louisburgh and Ballycastle (EUR 35,000), because Mulranny and Bangor Erris save little while Achill and Belmullet stay beyond them.
8. Evaluated every combination of offered districts on each run, since handing over a district at the end makes the one before it the end: Mulranny with Achill and Bangor Erris with Belmullet take 650 and 600 van-hours off their runs, more than Owenduff charges, while no combination on the Connemara, Cong or East Mayo runs saves money.
9. Forecast 2027: each district's stops a delivery day month by month from the plan's parcels at its own stops a parcel, each road section driven with the probability that some district beyond it has a stop; the year's net saving is EUR 50,000, where carrying the last twelve months' hours in proportion to parcels gives EUR 55,000.

No other list survives: NPS-3 4.1 counts the van-hours a hand-over takes off the runs, so time in district (which counts the road through Leenane and Letterfrack the Connemara van still drives) and allocation by stops or parcels are out; NPS-3 4.3 asks for the districts whose hand-over together lowers the year's cost most, so one-at-a-time pricing is out on the Achill and Erris runs; the fit on 2025 alone, on 2026 alone, with median drives, with annual rather than monthly stops, or a regression of run-day hours on the districts reached all give the same list and a net saving that rounds to EUR 50,000.
