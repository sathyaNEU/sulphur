"""task10 architecture 6: submission.md, the four answer blocks, drafted from figures.json so no figure is typed.
Every figure a block states is one an independent rebuild reproduces inside the band stated beside it. The
Supplementary Questions answer the prompt's sub-asks one by one and say how each file should look; the Critical
Components are the three findings the recommendation stands on, each from a different part of the work."""

ORDER = ["Ashcombe Road", "Charlecote Way", "Fenwick Street", "Hartwell Common"]
XLSX = "halverton_primary_capacity_2027-28.xlsx"
PPTX = "capex_review_2027-28.pptx"
TRADING = {"Corvane Flex Ltd": "Corvane Flex", "Quillon Energy Services Ltd": "Quillon Energy Services"}


def j(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def f1(v):
    return "%.1f" % v


def band(b):
    return "%.1f to %.1f" % (b[0], b[1])


def band2(b):
    return "%.2f to %.2f" % (b[0], b[1])


def write(F, path):
    Z, P, B, bt = F["zones"], F["providers"], F["bands"], F["backtest"]
    call, hold = F["call"], F["hold"]
    before, deliv, off, peak, q90 = F["r1_before"], F["r2_delivered"], F["r4_off_peak"], F["r5_peak"], F["r6_one_in_ten"]
    provs = sorted(P)
    cor, qui = P["Corvane Flex Ltd"], P["Quillon Energy Services Ltd"]
    car, R = F["careful"], F["routes"]
    late = [p for p in ORDER if Z[p]["peak_hh"] != "18:00"]
    early = [p for p in ORDER if Z[p]["peak_hh"] == "18:00"]
    part = [p for p in ORDER if Z[p]["per_scheduled"] - Z[p]["share"] > 0.05]
    pivot = [p for p in call if peak[p] <= Z[p]["firm"]]
    tot, ev = F["totals"], F["r1_evidence"]
    cv = F["conventions"]
    lost = lambda p: F["r8_bridge"]["%s, lost as load comes back" % p]
    na = lambda p: F["r8_bridge"]["%s, not available" % p]
    same_spread = cor["spread_pct"] == qui["spread_pct"]
    md = []
    md += ["## Tags", "",
           "**Domain:** Energy Systems & Utilities (load, price & renewable forecasting: a distribution network's design-day "
           "peak demand with contracted flexibility).  ",
           "**Analysis type:** Forecasting & Predictive Modeling.", ""]
    md += ["## Final Recommendation", "",
           "**Commit reinforcement at %s for winter 2027/28; %s stays within firm capacity on nine design days in ten with "
           "its 2027/28 contract (%s MW against %s).** With the contracts called in full on the design day the three peaks "
           "stay under %s on nine days in ten against %s of firm capacity, where crediting what past events delivered per "
           "megawatt scheduled off the 17:30 to 18:00 peak, with the megawatts of scatter the record shows, would reinforce "
           "%s alone: it reads %s's part calls as what a full call delivers (%s MW against %s), never rebuilds the day that "
           "then peaks after the window, and carries a small contract's megawatts of scatter to a contract more than twice "
           "the size (%s under %s MW, not %s)."
           % (j(call), j(hold), j(f1(q90[p]) for p in hold), j(f1(Z[p]["firm"]) for p in hold),
              j("%s MW" % f1(q90[p]) for p in call), j("%s MW" % f1(Z[p]["firm"]) for p in call), j(F["careful_call"]),
              late[0], f1(car[late[0]]["delivered"]), f1(deliv[late[0]]),
              pivot[0], f1(car[pivot[0]]["one_in_ten"]), f1(q90[pivot[0]])), ""]
    md += ["## Supplementary Questions", "",
           "### %s" % XLSX, "",
           "1. A Zones sheet with one row per flexibility zone (%s) and, across it, the megawatts contracted for 2027/28, "
           "the five figures below and firm capacity, each rounded to one decimal after the arithmetic (so a figure can "
           "differ by 0.1 from the difference of its rounded parts). Design-day demand before flexibility: %s."
           % (j(Z[p]["zone"] for p in ORDER), j("%s MW at %s (%s)" % (f1(before[p]), p, band(B["before"][p])) for p in ORDER)),
           "2. On the same sheet, the megawatts each 2027/28 contract delivers at 17:30 to 18:00 on the design day: %s."
           % j("%s MW at %s (%s; %s contracted)" % (f1(deliv[p]), p, band(B["delivered"][p]), f1(Z[p]["award"])) for p in ORDER),
           "3. The megawatts each contract takes off the day's peak: %s."
           % j("%s MW at %s (%s)" % (f1(off[p]), p, band(B["off_peak"][p])) for p in ORDER),
           "4. Each primary's expected design-day peak with its 2027/28 contract called in full: %s."
           % j("%s MW at %s (%s)" % (f1(peak[p]), p, band(B["peak"][p])) for p in ORDER),
           "5. The level each peak stays under on nine design days in ten, against firm capacity: %s."
           % j("%s MW at %s (%s) against %s" % (f1(q90[p]), p, band(B["one_in_ten"][p]), f1(Z[p]["firm"])) for p in ORDER),
           "6. A Bridge sheet from the megawatts contracted to the megawatts taken off the day's peak, zone by zone and for "
           "the four together: %s; of %s MW contracted, %s MW are not available on the design day, %s MW are delivered at "
           "17:30 to 18:00 and %s MW come off the peaks."
           % ("; ".join("%s %s MW contracted, %s not available, %s delivered, %s lost as load comes back after the "
                        "window, %s off the peak" % (p, f1(Z[p]["award"]), f1(na(p)), f1(deliv[p]), f1(lost(p)),
                                                     f1(deliv[p] - lost(p))) for p in ORDER),
              f1(tot["contracted"]), f1(tot["not_available"]), f1(tot["delivered"]), f1(tot["off_peak"])),
           "7. A Backtest sheet with one row per completed event of winter 2025/26 (megawatts predicted, delivered and "
           "the miss): fitted on winters 2023/24 and 2024/25 alone, the same approach is out by %.2f MW on average on "
           "what that winter's events delivered at 17:30 to 18:00 (%s)."
           % (F["r3_backtest"], band2(B["backtest"]["mae"])),
           "8. A clustered column chart on the Zones sheet: for each primary, demand before flexibility, the expected peak "
           "with flexibility and the nine-days-in-ten level beside firm capacity, in MW; the nine-days-in-ten column stands "
           "above firm capacity at %s and below it at %s." % (j(call), j(hold)),
           "", "### %s" % PPTX, "",
           "9. A short deck for the capital expenditure review that names %s as the primaries to reinforce for winter "
           "2027/28, states that %s stays within firm capacity on nine design days in ten, and carries the same chart."
           % (j(call), j(hold)), ""]
    md += ["## Critical Components", "",
           "1. On the days at or below minus %.1f C nearly every call outran what its provider had available, and the megawatts "
           "delivered ran at %s of the megawatts contracted at minus %.1f C, whatever was scheduled and in each of the three "
           "winters as the contracts grew. Per megawatt scheduled the same events show %s, where calls stopped short of the "
           "contract."
           % (cv["cold_days_at_or_below_minus"],
              j("**%.2f** for %s (%s)" % (F["c1_share"][p], TRADING[p], band2(B["share"][p])) for p in provs),
              cv["design_day_degrees_below_zero"], j("%.2f at %s" % (Z[p]["per_scheduled"], p) for p in part)),
           "2. Load comes back after the window: %s in the first half-hour for each megawatt delivered. Rebuilt half-hour by "
           "half-hour, %s's design day peaks in the half-hour to %s at **%s MW**, not at the %s MW of the half-hour to 18:00; "
           "%s keep their peak in the half-hour to 18:00."
           % (j("**%.2f MW** for %s (%s)" % (F["c2_comeback"][p], TRADING[p], band2(B["comeback"][p])) for p in provs),
              late[0], Z[late[0]]["peak_hh"], f1(peak[late[0]]), f1(Z[late[0]]["in_window"]), j(early)),
           "3. What a provider has available varies from one cold evening to the next by about %s, the same "
           "share at a small contract and a large one. Carried in that proportion to the 2027/28 megawatts with each "
           "primary's own day-to-day spread, %s, inside firm capacity on the expected day (%s MW against %s), stays under "
           "**%s MW** on nine design days in ten."
           % (("**%d per cent** of its level at both providers (%d to %d)" % (cor["spread_pct"], min(B["spread"][p][0] for p in provs),
                                                                              max(B["spread"][p][1] for p in provs))) if same_spread else
              j("**%d per cent** of its level for %s (%d to %d)" % (F["c3_spread"][p], TRADING[p], B["spread"][p][0], B["spread"][p][1]) for p in provs),
              pivot[0], f1(peak[pivot[0]]), f1(Z[pivot[0]]["firm"]), f1(q90[pivot[0]])), ""]
    steps = [
        "Cleaned the SCADA export (both point names mapped through the register, quality G half-hours kept once, UK local "
        "time), the dispatch log (each instruction at its latest revision, a cancelled one at no megawatts), the weather "
        "(each hour at its checked reading, averaged over the GMT day) and the switching log (each transfer from the "
        "operation that closed the open point to the one that restored it).",
        "Design-day demand before flexibility (guideline 2 to 5): each zone primary's 2025/26 daily peaks on working "
        "weekdays outside 24 December to 2 January, outside its scheduled days and outside days with a logged transfer at "
        "the primary, corrected to minus %.1f C on a straight line in heating degrees and grown by the DFES rates and the "
        "qualifying connections: %s. Those days reach no colder than plus %.1f C, so the straight line was checked where "
        "the record allows: in the hours before the service window, which the scheduled days do carry, the line fitted on "
        "the mild days lands the days at or below 0 C within %d per cent at every zone primary, and a curve fitted on the "
        "same days misses them by more."
        % (cv["design_day_degrees_below_zero"], j("%s MW at %s" % (f1(before[p]), p) for p in ORDER),
           ev["coldest_unscheduled_c"], ev["line_within_pct"]),
        "Measured each completed event's megawatts delivered in the half-hours ending 17:30 and 18:00 against a "
        "weather-adjusted baseline fitted on the primary's other working weekdays, days with a logged transfer left out.",
        "The hurried reading: megawatts delivered per megawatt scheduled, regressed on temperature zone by zone and read "
        "at minus %.1f C, applied to the megawatts contracted: %s. Taken off the 17:30 to 18:00 peak, it lets %s hold at "
        "%s MW."
        % (cv["design_day_degrees_below_zero"], j("%s MW at %s" % (f1(car[p]["delivered"]), p) for p in ORDER),
           late[0], f1(car[late[0]]["peak"])),
        "What the record shows: on mild days the megawatts scheduled were delivered; on the cold days the megawatts "
        "delivered stopped at a share of the megawatts contracted that falls as it gets colder, the same share at both of "
        "a provider's zones and in all three winters while the contracts grew, and on equally cold days scheduling more "
        "did not deliver more. Regressed on temperature over the days at or below minus %.1f C, that share is %.2f for "
        "Corvane Flex and %.2f for Quillon Energy Services at minus %.1f C, so the 2027/28 contracts deliver %s."
        % (cv["cold_days_at_or_below_minus"], cor["share"], qui["share"], cv["design_day_degrees_below_zero"],
           j("%s MW" % f1(deliv[p]) for p in ORDER)),
        "Backtest: fitted on winters 2023/24 and 2024/25 alone and applied to winter 2025/26's larger contracts, the lesser "
        "of the megawatts scheduled and that share of the megawatts contracted is out by %.2f MW on average. The hurried "
        "reading passes the same test (%.2f MW), because last winter's calls sat as far below their contracts as the calls "
        "it was fitted on: a held-out winter cannot tell the two readings apart, and what does is the step above."
        % (F["r3_backtest"], F["careful_backtest"]["mae"]),
        "The design day half-hour by half-hour (guideline 6 takes the day's highest half-hour with the service delivered "
        "through its window, 16:00 to 19:30 in the award notice; the half-hours ending 17:30 and 18:00 are how a contract's "
        "megawatts are quoted, not the extent of the credit): each half-hour's 2025/26 level corrected to the design "
        "condition and grown in the proportion the peak grows, less the window's reduction (the megawatts delivered through "
        "each half-hour of the window as the events show them), plus what comes back after it (%.2f and %.2f MW in the two "
        "half-hours after the window for each "
        "megawatt Corvane Flex delivers, %.2f and %.2f for Quillon Energy Services). %s peaks in the half-hour to %s at %s "
        "MW (%s MW in the half-hour to 18:00); the others peak in the half-hour to 18:00: %s."
        % (cor["back_first"], cor["back_second"], qui["back_first"], qui["back_second"], late[0], Z[late[0]]["peak_hh"],
           f1(peak[late[0]]), f1(Z[late[0]]["in_window"]), j("%s MW at %s" % (f1(peak[p]), p) for p in early)),
        "The megawatts off the day's peak are demand before flexibility less that peak: %s; the bridge from %s MW "
        "contracted loses %s MW to what is not available and %s MW to the load that comes back."
        % (j("%s MW at %s" % (f1(off[p]), p) for p in ORDER), f1(tot["contracted"]), f1(tot["not_available"]),
           f1(tot["comeback_loss"])),
        "One day in ten: the scatter of delivered over contracted about its line on the cold days, less what the same "
        "measurement shows on days with nothing scheduled, is about %s; it is the same share "
        "at a small contract and a large one, so it is carried in proportion to the 2027/28 megawatts, with each primary's "
        "day-to-day spread about its weather correction, and the day recomputed half-hour by half-hour: %s. The megawatts "
        "of scatter the record shows, carried unchanged, would put %s under %s MW."
        % (("%d per cent of the level at both providers" % cor["spread_pct"]) if same_spread else
           ("%d and %d per cent of the level" % (cor["spread_pct"], qui["spread_pct"])), j("%s MW at %s" % (f1(q90[p]), p) for p in ORDER),
           pivot[0], f1(car[pivot[0]]["one_in_ten"])),
        "Set against firm capacity (guideline 7): %s would exceed it on more than one design day in ten (their "
        "nine-days-in-ten levels stand %s over it); %s's stands %s MW inside it."
        % (j(call), j("%s MW" % f1(Z[p]["over_by"]) for p in call), j(hold), j(f1(Z[p]["inside_by"]) for p in hold)),
    ]
    md += ["## Step-by-Step", ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(steps)] + [""]

    def route(key):
        v = R[key]
        return j(v) if v else "nothing"

    md += ["No other conclusion survives the files. The megawatts contracted taken at face value would reinforce %s. "
           "Megawatts delivered per megawatt scheduled carried to the contract and taken off the 17:30 to 18:00 peak "
           "reinforces %s alone with the record's megawatts of scatter and %s with the scatter in proportion: at %s the "
           "cold-day calls stopped short of the contract, so the megawatts delivered there read high per megawatt "
           "scheduled, and the day's peak after the window is never rebuilt. The megawatts the 2025/26 contracts made "
           "available, carried unchanged, would reinforce %s, but the megawatts delivered grew with the contracts in every "
           "zone. The available share with the expected day alone would leave %s out (%s MW against %s); on nine design "
           "days in ten it stays under %s MW. A curved weather correction is not carried, because the cold days the record "
           "does hold sit on the straight line. Every variant tried (the cold days taken at or below 0, minus 1.5 or minus "
           "2 C, a curved line through the share, each zone on its own, the scatter as measured, a heating base of 14 or 17 C, "
           "a baseline with a slope each winter, with weekday levels or scaled to the day's own level before the window, a "
           "met call taken as a floor or left out, the megawatts fitted over every event, a cancelled instruction's day kept, "
           "the megawatts delivered carried to the award at the rate the three winters' record itself gives) reinforces the "
           "same three primaries."
           % (route("the megawatts contracted taken at face value"),
              route("megawatts delivered per megawatt scheduled, the record's megawatts of scatter unchanged"),
              route("megawatts delivered per megawatt scheduled, the scatter in proportion, the credit off the 17:30 to 18:00 peak"),
              j(part), ("all four" if len(R["the megawatts the 2025/26 contracts made available carried unchanged"]) == 4 else
                        route("the megawatts the 2025/26 contracts made available carried unchanged")),
              pivot[0], f1(peak[pivot[0]]), f1(Z[pivot[0]]["firm"]), f1(q90[pivot[0]]))]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
