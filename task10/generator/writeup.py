"""task10 architecture 7: submission.md, the four answer blocks, drafted from figures.json so no figure is typed.
Every figure a block states is one an independent rebuild reproduces inside the band stated beside it. The
Supplementary Questions answer the prompt's sub-asks one by one and say how each file should look; the Critical
Components are the five results every valid assessment has to compute, from different parts of the work."""

XLSX = "halverton_primary_assessment_2027-28.xlsx"
PPTX = "capex_review_2027-28.pptx"
CAREFUL = "careful but hurried: the line, the type's established share, the planned dates"
LINE = "each evening half-hour on a straight line through the days no service ran, three winters"
MATURE = "the same customers at their type's established share"
OBSERVED = "every customer at what the latest months show, no further build-up"
PLANNED = "the sites still to come on their planned dates"
POOLED = "the sites still to come on the register's record across every class"
NOREPLAY = "the delivery taken off the 17:00 to 18:00 peak"
DONE = "each class's record read from the sites commissioned alone"


def j(items):
    items = list(items)
    if not items:
        return "none"
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def f1(v):
    return "%.1f" % v


def f2(v):
    return "%.2f" % v


def b1(b):
    return "%.1f to %.1f" % (b[0], b[1])


def b2(b):
    return "%.2f to %.2f" % (b[0], b[1])


def b0(b):
    return "%d to %d" % (b[0], b[1])


def write(F, path):
    names, Z, B = F["order"], F["zones"], F["bands_by_result"]
    call, hold = F["call"], F["hold"]
    d26, conn, before, insvc = F["r1_demand_2526"], F["r2_connections"], F["r3_before"], F["r4_in_service"]
    share, deliv, back, peak, q90, over = (F["r5_share"], F["r6_delivered"], F["r7_comeback"], F["r8_peak"],
                                           F["r9_one_in_ten"], F["r10_share_over"])
    car, R, RF = F["careful"], F["routes"], F["route_figures"]
    provs = F["providers_order"]
    cv = F["conventions"]
    late = [n for n in names if Z[n]["peak_hh"] not in ("17:30", "18:00")]

    def each(tab, band=None, unit=" MW", fmt=f1, bfmt=b1, who=names):
        return "; ".join("%s %s%s%s" % (n, fmt(tab[n]), unit, (" (%s)" % bfmt(band[n])) if band else "") for n in who)

    md = []
    md += ["## Tags", "",
           "**Domain:** Energy Systems & Utilities (load, price & renewable forecasting: a distribution network's design-day "
           "peak demand with contracted flexibility).  ",
           "**Analysis type:** Forecasting & Predictive Modeling.", ""]
    hc = car["R11"]
    md += ["## Final Recommendation", "",
           "**Commit reinforcement at %s for winter 2027/28; %s within firm capacity on nine design days in ten with its "
           "2027/28 contract (%s MW against %s).** With each contract instructed in full on the design day the %s peaks stay "
           "under %s on nine days in ten against %s of firm capacity. The assessment a careful analyst in a hurry files "
           "(each evening half-hour on a straight line through the days no service ran, the customers due after the latest "
           "winter at their type's established share of agreed capacity, the sites still to come on their planned dates) "
           "would commit %s instead: it puts Dunmore Street's 2025/26 design-day demand at %s MW where the mornings give %s, "
           "counts %s MW of customers at Charlecote Way where the register's customers add %s and %s MW at Hartwell Common "
           "where they add %s, and credits Fenwick Street with %s MW in service where its sites' record gives %s."
           % (j(call), j(hold) + (" stays" if len(hold) == 1 else " stay"), j(f1(q90[n]) for n in hold),
              j(f1(Z[n]["firm"]) for n in hold), {4: "four", 3: "three", 2: "two", 5: "five"}.get(len(call), str(len(call))),
              j("%s MW" % f1(q90[n]) for n in call), j("%s MW" % f1(Z[n]["firm"]) for n in call), j(hc),
              f1(car["R1"]["Dunmore Street"]), f1(d26["Dunmore Street"]),
              f1(car["R2"]["Charlecote Way"]), f1(conn["Charlecote Way"]),
              f1(car["R2"]["Hartwell Common"]), f1(conn["Hartwell Common"]),
              f1(car["R4"]["Fenwick Street"]), f1(insvc["Fenwick Street"])), ""]

    md += ["## Supplementary Questions", "", "### %s" % XLSX, "",
           "1. Sheet Primaries holds one row per zone primary in name order (%s), with the constraint managed zone, the "
           "provider, the design-day demand in winter 2025/26, the megawatts the growth register's customers add, the "
           "design-day demand before flexibility in winter 2027/28, the megawatts contracted, the megawatts in service on "
           "%s, the share of them available on the design day, the megawatts delivered between 17:00 and 18:00, the "
           "half-hour of the day's peak, the expected peak, the level it stays under on nine design days in ten, firm "
           "capacity, the share of design days over firm capacity and Yes or No for reinforcement; megawatts to one decimal "
           "place and the share of days to the nearest whole per cent. Under the table a clustered column chart shows, for "
           "each primary, demand before flexibility, the expected peak, the nine-days-in-ten level and firm capacity. Sheets "
           "Demand, Customers, Sites and Routes carry the working: the cold end of each primary's demand, the customers "
           "behind each connections figure, the sites still to come by asset class, and what each shortcut would have "
           "committed." % (j(names), cv["assessment_date"]),
           "2. Design-day demand before flexibility in winter 2027/28 (reproducible range in brackets): %s."
           % each(before, B["R3"]),
           "3. Megawatts each contract can be expected to deliver between 17:00 and 18:00 on the design day: %s."
           % each(deliv, B["R6"]),
           "4. Expected peak with the service instructed in full: %s. %s"
           % (each(peak, B["R8"]),
              ("%s peaks in the half-hour ending %s, after the service window; the others peak inside it."
               % (j(late), Z[late[0]]["peak_hh"])) if late else "Every primary peaks inside the service window."),
           "5. Level the peak stays under on nine design days in ten, against firm capacity: %s."
           % "; ".join("%s %s MW (%s) against %s" % (n, f1(q90[n]), b1(B["R9"][n]), f1(Z[n]["firm"])) for n in names),
           "6. Share of design days over firm capacity: %s. Reinforce: %s; not %s."
           % ("; ".join("%s %d per cent (%s)" % (n, over[n], b0(B["R10"][n])) for n in names), j(call), j(hold)),
           "", "### %s" % PPTX, "",
           "7. Five slides: the list to commit and the list to hold with each nine-days-in-ten level against firm capacity; "
           "a clustered column chart of demand before flexibility, the expected peak, the nine-days-in-ten level and firm "
           "capacity for each primary, every bar carrying its value; the demand side (each primary's 2025/26 design-day "
           "demand, what the customers add and the 2027/28 figure); the flexibility side (megawatts contracted, in service "
           "and delivered for each primary); and the decision with each primary's share of design days over firm capacity.",
           ""]

    md += ["## Critical Components", "",
           "1. Design-day demand in winter 2025/26, every working weekday at minus %.1f C with or without a service: %s."
           % (cv["design_day_degrees_below_zero"], "; ".join("%s **%s MW** (%s)" % (n, f1(d26[n]), b1(B["R1"][n])) for n in names)),
           "2. Megawatts the growth register's customers add between %s and %s: %s."
           % (cv["latest_winter_date"], cv["assessment_date"],
              "; ".join("%s **%s MW** (%s)" % (n, f1(conn[n]), b1(B["R2"][n])) for n in names)),
           "3. Megawatts each provider can be expected to have in service on %s: %s."
           % (cv["assessment_date"], "; ".join("%s **%s MW** (%s) of %s contracted" % (n, f1(insvc[n]), b1(B["R4"][n]),
                                                                                     f1(Z[n]["contracted"])) for n in names)),
           "4. Share of its megawatts in service each provider has available on the design day: %s."
           % "; ".join("%s **%s** (%s)" % (p, f2(share[p]), b2(B["R5"][p])) for p in provs),
           "5. Megawatts that come back in the four half-hours after the window for each megawatt delivered: %s%s"
           % ("; ".join("%s **%s** (%s)" % (p, f2(back[p]), b2(B["R7"][p])) for p in provs),
              ("; this is what moves %s's peak to the half-hour ending %s." % (late[0], Z[late[0]]["peak_hh"])) if late else "."),
           ""]

    dz = Z["Dunmore Street"]
    ce = F["cold_end"]["Dunmore Street"]
    fz = Z["Fenwick Street"]
    cls = F["classes"]
    steps = [
        "Cleaned the files: `primary_demand_halfhourly_2023-2026.csv` mapped to asset codes through both point names in "
        "`primary_substation_register.xlsx`, quality G rows kept and the re-sent overlap counted once; the latest "
        "revision of each instruction in `flexibility_events_2023-2026.csv`; the checked version of each hour in "
        "`halverton_weather_hourly_2023-2026.csv`; days with a transfer in `control_room_switching_log_2023-2026.csv` "
        "left out at both primaries.",
        "Design-day demand, winter 2025/26 (guideline 2 and 3: every working weekday at minus %.1f C, with or without a "
        "service). The service ran on the cold days: at Dunmore Street no working weekday without one in 2025/26 was colder "
        "than %s C, and a straight line through such days carried to the design temperature gives %s MW there. The "
        "half-hours ending 07:00 to 15:30 are never inside a service window, so every one of the %d working weekdays on "
        "record shows them, %d at or below 0 C: at Dunmore Street they rise %s MW per degree colder above about %s C and "
        "%s below. Each evening half-hour was tied to the morning on the days no service ran and read at the morning "
        "the design temperature gives: %s."
        % (cv["design_day_degrees_below_zero"], f1(dz["coldest_without_service_2526"]), f1(car["R1"]["Dunmore Street"]),
           dz["working_weekdays"], dz["at_or_below_freezing"], f2(ce["per_degree_above"]), f1(ce["knee_c"]),
           f2(ce["per_degree_below"]), each(d26)),
        "Customers (guideline 4: what the customers on `load_growth_register_2026-27.xlsx` will have added between the "
        "two assessment dates). Joined the register to `hh_customer_demand_monthly_2021-2026.csv` on the meter point, "
        "feeders to primaries through `network_feeders_11kv.xlsx`. A customer's demand as a share of its agreed capacity "
        "depends on its type and takes two to three years to build up, so each customer on supply was carried from its own "
        "latest months up its type's build-up to %s, and each customer still to connect was put on its type's. Counting "
        "only the customers due after the latest winter at their type's established share gives Charlecote Way %s MW and "
        "Hartwell Common %s; the register's customers add %s."
        % (cv["assessment_date"], f1(car["R2"]["Charlecote Way"]), f1(car["R2"]["Hartwell Common"]), each(conn)),
        "Demand before flexibility, winter 2027/28: the 2025/26 figure grown at the DFES rates in "
        "`primary_substation_register.xlsx` for two years, plus the customers, every half-hour in the peak's proportion: %s."
        % each(before),
        "Megawatts in service on %s (guideline 6). `flexibility_asset_register_2026-11-04.csv` holds %d sites across the "
        "licence area. For the sites whose planned date has passed, the share in service by days since that date was read "
        "by asset class, sites withdrawn counted as never commissioned: %s. Each site still to come at the five zones was "
        "given its class's chance of being in service by the assessment date, given how long it is already overdue. On "
        "their planned dates Fenwick Street's sites would give %s MW in service; on their classes' record, %s. Read from "
        "the sites commissioned alone the classes' record would give %s MW there and %s at Ashcombe Road, but %d of the %d "
        "process load sites whose planned date has passed were still to come at the extract and %d had been withdrawn, and "
        "they are part of the record. All five: %s."
        % (cv["assessment_date"], F["pack"]["register_sites"],
           "; ".join("%s a median of %d days late" % (c.lower() if c != "HVAC" and not c.startswith("EV") else c,
                                                       v["median_days_late"]) for c, v in cls.items()),
           f1(car["R4"]["Fenwick Street"]), f1(insvc["Fenwick Street"]),
           f1(RF[DONE]["Fenwick Street"]["in_service"]), f1(RF[DONE]["Ashcombe Road"]["in_service"]),
           cls["Process load"]["sites"] - cls["Process load"]["commissioned"] - cls["Process load"]["withdrawn"],
           cls["Process load"]["sites"], cls["Process load"]["withdrawn"], each(insvc)),
        "Share available on the design day. Each completed event's megawatts were measured as the day's evening without a "
        "service (from its own morning) less the metered demand, in the half-hours ending 17:30 and 18:00, and set against "
        "the megawatts the provider had in service that day. An event that met its instruction shows only a floor; the "
        "events that fell short show the share itself, which falls as the day gets colder: %s at the design temperature."
        % "; ".join("%s %s" % (p, f2(share[p])) for p in provs),
        "Megawatts delivered between 17:00 and 18:00: the share times the megawatts in service: %s." % each(deliv),
        "The day with the service. The reduction through the window and the load that comes back in the four half-hours "
        "after it were read from the same events (%s of a megawatt back per megawatt delivered) and the design day rebuilt "
        "half-hour by half-hour. Taking the delivery off the 17:00 to 18:00 peak would hold Ashcombe Road at %s MW on nine "
        "days in ten; rebuilt, its peak moves to the half-hour ending %s. Expected peaks: %s."
        % (j("%s %s" % (p, f2(back[p])) for p in provs), f1(RF[NOREPLAY]["Ashcombe Road"]["one_in_ten"]),
           Z["Ashcombe Road"]["peak_hh"], each(peak)),
        "Nine design days in ten (guideline 7). Design days were drawn from the day-to-day spread of demand the mornings "
        "show and of what each provider had available, and each day's highest half-hour taken: %s. Share of design days "
        "over firm capacity: %s."
        % ("; ".join("%s %s MW against %s" % (n, f1(q90[n]), f1(Z[n]["firm"])) for n in names),
           "; ".join("%s %d per cent" % (n, over[n]) for n in names)),
        "Decision: reinforce %s; %s within firm capacity." % (j(call), j(hold) + (" stays" if len(hold) == 1 else " stay")),
    ]
    md += ["## Step-by-Step", ""]
    md += ["%d. %s" % (i + 1, s) for i, s in enumerate(steps)]
    md += ["",
           "No other list survives the files. A straight line through the days without a service would drop Dunmore Street "
           "(%s MW on nine days in ten against %s of firm capacity), and the mornings of %d days at or below 0 C rule it out. "
           "Reading the connections as the customers due after the latest winter would drop Charlecote Way (%s MW) and add "
           "Hartwell Common (%s MW), and so would holding every customer at what its latest months show (%s and %s MW); the "
           "monthly readings of customers at every age rule both out. The megawatts contracted, the planned dates or one "
           "commissioning record across every asset class would drop Fenwick Street (%s, %s and %s MW); the register's own "
           "record by class rules them out, read with the sites still to come and the sites withdrawn in it. Each of the %d "
           "variants of this assessment's own choices commits the same four."
           % (f1(RF[LINE]["Dunmore Street"]["one_in_ten"]), f1(dz["firm"]), dz["at_or_below_freezing"],
              f1(RF[MATURE]["Charlecote Way"]["one_in_ten"]), f1(RF[MATURE]["Hartwell Common"]["one_in_ten"]),
              f1(RF[OBSERVED]["Charlecote Way"]["one_in_ten"]), f1(RF[OBSERVED]["Hartwell Common"]["one_in_ten"]),
              f1(RF["the megawatts contracted, at the share of megawatts in service"]["Fenwick Street"]["one_in_ten"]),
              f1(RF[PLANNED]["Fenwick Street"]["one_in_ten"]), f1(RF[POOLED]["Fenwick Street"]["one_in_ten"]),
              F["variants"]["n"]), ""]
    open(path, "w").write("\n".join(md))
