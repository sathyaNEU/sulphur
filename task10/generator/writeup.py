"""task10 architecture 6: submission.md, the four answer blocks, drafted from figures.json so no figure is typed.
Every figure a block states is one an independent rebuild reproduces at the stated precision."""

ORDER = ["Ashcombe Road", "Charlecote Way", "Fenwick Street", "Hartwell Common"]


def j(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def f1(v):
    return "%.1f" % v


def band(b):
    return "%.1f to %.1f" % (b[0], b[1])


def write(F, path):
    Z, P, B, bt = F["zones"], F["providers"], F["bands"], F["backtest"]
    call, hold = F["call"], F["hold"]
    before, deliv, off, peak, q90 = F["r1_before"], F["r2_delivered"], F["r4_off_peak"], F["r5_peak"], F["r6_one_in_ten"]
    cor, qui = P["Corvane Flex Ltd"], P["Quillon Energy Services Ltd"]
    car = F["careful"]
    late = [p for p in ORDER if Z[p]["peak_hh"] != "18:00"]
    early = [p for p in ORDER if Z[p]["peak_hh"] == "18:00"]
    part = [p for p in ORDER if Z[p]["per_scheduled"] - Z[p]["share"] > 0.05]
    tot = F["totals"]
    md = []
    md += ["## Tags", "",
           "**Domain:** Energy Systems & Utilities (load, price & renewable forecasting: a distribution network's design-day "
           "peak demand with contracted flexibility).  ",
           "**Analysis type:** Forecasting & Predictive Modeling.", ""]
    md += ["## Final Recommendation", "",
           "**Commit reinforcement at %s for winter 2027/28; %s stays within firm capacity on nine design days in ten with "
           "its 2027/28 contract.** With the contracts called in full on the design day, the peaks stay under %s on nine "
           "days in ten against %s of firm capacity (%s %s MW against %s). Crediting what past events delivered per megawatt "
           "scheduled, taken off the 17:30 to 18:00 peak with the fit's own range, would reinforce %s alone: it reads "
           "%s's part calls as what a full call delivers, and it reads %s's expected day (%s MW) as its one in ten."
           % (j(call), j(hold), j("%s MW" % f1(q90[p]) for p in call), j("%s MW" % f1(Z[p]["firm"]) for p in call),
              j(hold), j(f1(q90[p]) for p in hold), j(f1(Z[p]["firm"]) for p in hold), j(F["careful_call"]),
              "Ashcombe Road", "Fenwick Street", f1(peak["Fenwick Street"])), ""]
    md += ["## Supplementary Questions", "",
           "### The spreadsheet", "",
           "1. A Zones sheet with one row per flexibility zone (%s), giving the megawatts contracted for 2027/28, firm "
           "capacity and each primary's design-day demand before flexibility: %s."
           % (j(Z[p]["zone"] for p in ORDER), j("%s MW at %s (%s)" % (f1(before[p]), p, band(B["before"][p])) for p in ORDER)),
           "2. A Backtest sheet: the same approach fitted on winters 2023/24 and 2024/25 and set against winter 2025/26's "
           "%d completed events is out by %.2f MW on average (%.2f to %.2f), and %d of that winter's %d events on days "
           "below 0 C fall inside the %d per cent range it gives (%d to %d)."
           % (bt["n"], bt["mae"], B["backtest"]["mae"][0], B["backtest"]["mae"][1], bt["n_inside"], bt["n_cold"],
              bt["range_pct"], B["backtest"]["inside"][0], B["backtest"]["inside"][1]),
           "3. Each primary's expected design-day peak with its 2027/28 contract called in full: %s."
           % j("%s MW at %s (%s)" % (f1(peak[p]), p, band(B["peak"][p])) for p in ORDER),
           "4. A Bridge sheet from the megawatts contracted to the megawatts taken off the day's peak, zone by zone and for "
           "the four together: %s; of %s MW contracted, %s MW are not available on the design day, %s MW are delivered at "
           "17:30 to 18:00 and %s MW come off the peaks."
           % ("; ".join("%s %s MW contracted, %s not available, %s delivered, %s lost as load comes back after the "
                        "window, %s off the peak" % (p, f1(Z[p]["award"]), f1(F["r8_bridge"]["%s, not available" % p]),
                                                     f1(deliv[p]), f1(F["r8_bridge"]["%s, lost as load comes back" % p]),
                                                     f1(off[p])) for p in ORDER),
              f1(tot["contracted"]), f1(tot["not_available"]), f1(tot["delivered"]), f1(tot["off_peak"])),
           "5. A clustered column chart on the Zones sheet: for each primary, demand before flexibility, the expected peak "
           "with flexibility and the nine-days-in-ten level beside firm capacity, in MW; the nine-days-in-ten column stands "
           "above firm capacity at %s and below it at %s." % (j(call), j(hold)),
           "", "### The slides", "",
           "6. A short deck for the capital expenditure review that names %s as the primaries to reinforce for winter "
           "2027/28, states that %s stays within firm capacity on nine design days in ten, and carries the same chart."
           % (j(call), j(hold)), ""]
    md += ["## Critical Components", "",
           "1. On the days at or below minus %.1f C every call outran what its provider had available (all but %d of %d "
           "events fell short of the megawatts scheduled), and the megawatts delivered ran at **%.2f** (Corvane Flex) and "
           "**%.2f** (Quillon Energy Services) of the megawatts contracted at minus %.1f C, whatever was scheduled. Called "
           "in full, the 2027/28 contracts deliver %s at 17:30 to 18:00. Per megawatt scheduled the same events show %s, "
           "where calls stopped short of the contract."
           % (F["conventions"]["cold_days_at_or_below_minus"], cor["cold_met"] + qui["cold_met"], cor["n_cold"] + qui["n_cold"],
              cor["share"], qui["share"], F["conventions"]["design_day_degrees_below_zero"],
              j("**%s MW** at %s (%s; %s contracted)" % (f1(deliv[p]), p, band(B["delivered"][p]), f1(Z[p]["award"])) for p in ORDER),
              j("%.2f at %s" % (Z[p]["per_scheduled"], p) for p in part)),
           "2. Load comes back after the window: %.2f MW (Corvane Flex) and %.2f MW (Quillon Energy Services) in the first "
           "half-hour for each megawatt delivered. With %s MW delivered, %s's design day peaks in the half-hour to %s, so "
           "its contract takes **%s MW** off the day's peak (%s); %s keep their peak in the half-hour to 18:00 and take %s "
           "off."
           % (cor["back_first"], qui["back_first"], f1(deliv[late[0]]), late[0], Z[late[0]]["peak_hh"], f1(off[late[0]]),
              band(B["off_peak"][late[0]]), j(early),
              j("**%s MW** (%s)" % (f1(off[p]), band(B["off_peak"][p])) for p in early)),
           "3. What a provider has available varies from one cold evening to the next by about %s of its level. Carried at "
           "that proportion to the 2027/28 megawatts, with each primary's own day-to-day spread, the design-day peaks stay "
           "under %s on nine design days in ten."
           % (("%d per cent at both providers" % cor["spread_pct"]) if cor["spread_pct"] == qui["spread_pct"] else
              ("%d per cent (Corvane Flex) and %d per cent (Quillon Energy Services)" % (cor["spread_pct"], qui["spread_pct"])),
              j("**%s MW** at %s (%s)" % (f1(q90[p]), p, band(B["one_in_ten"][p])) for p in ORDER)), ""]
    steps = [
        "Cleaned the SCADA export (both point names mapped through the register, quality G half-hours kept once, UK local "
        "time), the dispatch log (each instruction at its latest revision, a cancelled one at no megawatts), the weather "
        "(each hour at its checked reading, averaged over the GMT day) and the switching log (each transfer from the "
        "operation that closed the open point to the one that restored it): %d completed events at the four zones."
        % F["record"]["completed_total"],
        "Design-day demand before flexibility (guideline 2 to 5): each zone primary's 2025/26 daily peaks on working "
        "weekdays outside 24 December to 2 January, outside its scheduled days and outside days with a logged transfer at "
        "the primary, corrected to minus %.1f C and grown by the DFES rates and the qualifying connections: %s."
        % (F["conventions"]["design_day_degrees_below_zero"], j("%s MW at %s" % (f1(before[p]), p) for p in ORDER)),
        "Measured each completed event's megawatts delivered in the half-hours ending 17:30 and 18:00 against a "
        "weather-adjusted baseline fitted on the primary's other working weekdays, days with a logged transfer left out.",
        "The hurried reading: megawatts delivered per megawatt scheduled, regressed on temperature zone by zone and read "
        "at minus %.1f C, applied to the megawatts contracted: %s. It lets %s."
        % (F["conventions"]["design_day_degrees_below_zero"],
           j("%s MW at %s" % (f1(car[p]["delivered"]), p) for p in ORDER),
           "Ashcombe Road hold at %s MW" % f1(car["Ashcombe Road"]["peak"])),
        "What the record shows: on mild days the megawatts scheduled were delivered; on the cold days the megawatts "
        "delivered stopped at a share of the megawatts contracted that falls as it gets colder, the same share at both of "
        "a provider's zones and in all three winters while the contracts grew. Regressed on temperature over the days at or "
        "below minus %.1f C (%d and %d events), that share is %.2f for Corvane Flex and %.2f for Quillon Energy Services at "
        "minus %.1f C, so the 2027/28 contracts deliver %s."
        % (F["conventions"]["cold_days_at_or_below_minus"], cor["n_cold"], qui["n_cold"], cor["share"], qui["share"],
           F["conventions"]["design_day_degrees_below_zero"], j("%s MW" % f1(deliv[p]) for p in ORDER)),
        "Backtest: fitted on winters 2023/24 and 2024/25 alone and applied to winter 2025/26's larger contracts, the lesser "
        "of the megawatts scheduled and that share of the megawatts contracted is out by %.2f MW on average over %d events, "
        "and %d of the %d events on days below 0 C fall inside its %d per cent range."
        % (bt["mae"], bt["n"], bt["n_inside"], bt["n_cold"], bt["range_pct"]),
        "The design day half-hour by half-hour: each half-hour's 2025/26 level corrected to the design condition and grown "
        "in the proportion the peak grows, less the window's reduction (the megawatts delivered through the window as the "
        "events show them), plus what comes back after it (%.2f and %.2f MW in the two half-hours after the window for each "
        "megawatt Corvane Flex delivers, %.2f and %.2f for Quillon Energy Services). %s peaks in the half-hour to %s at %s "
        "MW (%s MW in the half-hour to 18:00); the others peak in the half-hour to 18:00: %s."
        % (cor["back_first"], cor["back_second"], qui["back_first"], qui["back_second"], late[0], Z[late[0]]["peak_hh"],
           f1(peak[late[0]]), f1(Z[late[0]]["in_window"]), j("%s MW at %s" % (f1(peak[p]), p) for p in early)),
        "The megawatts off the day's peak are demand before flexibility less that peak: %s; the bridge from %s MW "
        "contracted loses %s MW to what is not available and %s MW to the load that comes back."
        % (j("%s MW at %s" % (f1(off[p]), p) for p in ORDER), f1(tot["contracted"]), f1(tot["not_available"]),
           f1(tot["comeback_loss"])),
        "One day in ten: the scatter of delivered over contracted about its line on the cold days, less what the same "
        "measurement shows on days with nothing scheduled, is about %d and %d per cent of the level; it is the same share "
        "at a small contract and a large one, so it is carried in proportion to the 2027/28 megawatts, with each primary's "
        "day-to-day spread about its weather correction, and the day recomputed half-hour by half-hour: %s."
        % (cor["spread_pct"], qui["spread_pct"], j("%s MW at %s" % (f1(q90[p]), p) for p in ORDER)),
        "Set against firm capacity (guideline 7): %s exceed it on more than one design day in ten, by %s; %s stays %s MW "
        "inside it at that level."
        % (j(call), j("%s MW at %s" % (f1(Z[p]["over_by"]), p) for p in call), j(hold),
           j(f1(Z[p]["inside_by"]) for p in hold)),
    ]
    md += ["## Step-by-Step", ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(steps)] + [""]
    md += ["No other conclusion survives the files. The megawatts contracted taken at face value would reinforce nothing. "
           "Megawatts delivered per megawatt scheduled carried to the contract, with the fit's own range, reinforces %s "
           "alone: at Ashcombe Road and Charlecote Way the cold-day calls stopped at about four fifths of the contract, so "
           "the megawatts delivered there read high per megawatt scheduled, and on equally cold days scheduling more did not "
           "deliver more. The megawatts the 2025/26 contracts made available, carried unchanged, would reinforce all four, "
           "but the megawatts delivered grew with the contracts in every zone, which the backtest on the larger 2025/26 "
           "contracts confirms. The expected day alone would leave %s out (%s MW against %s); on nine design days in ten it "
           "stays under %s MW, because what Quillon Energy Services has available on a cold evening varies by about %d per "
           "cent. Every variant tried (the cold days taken at or below 0, minus 1.5 or minus 2 C, a curved line, each zone "
           "on its own, the scatter as measured, a heating base of 14 or 17 C) reinforces the same three primaries."
           % (j(F["careful_call"]), "Fenwick Street", f1(peak["Fenwick Street"]), f1(Z["Fenwick Street"]["firm"]),
              f1(q90["Fenwick Street"]), qui["spread_pct"])]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
