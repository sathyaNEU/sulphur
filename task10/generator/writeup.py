"""task10 architecture 7: submission.md, the four answer blocks, drafted from figures.json so no figure is typed.
Every figure a block states is one an independent rebuild reproduces inside the band stated beside it. The
Supplementary Questions answer the prompt's sub-asks one by one and say how each file should look; the Critical
Components are the five results every valid assessment has to compute, from different parts of the work."""

XLSX = "halverton_primary_assessment_2027-28.xlsx"
PPTX = "capex_review_2027-28.pptx"
CAREFUL = "careful but hurried: the mornings on a straight line, the come-back as the record's megawatts"
LINE = "each evening half-hour on a straight line through the days no service ran, three winters"
MATURE = "the same customers at their type's established share"
OBSERVED = "every customer at what the latest months show, no further build-up"
PLANNED = "the sites still to come on their planned dates"
POOLED = "the sites still to come on the register's record across every class"
NOREPLAY = "the delivery taken off the 17:00 to 18:00 peak"
DONE = "each class's record read from the sites commissioned alone"
FIXED = "the come-back as the megawatts the record's events showed, whatever they delivered"
LINEAR_M = "the mornings on a straight line in temperature"
ZONE_RATIO = "a further megawatt at the share of its contract the zone will have in service"
LINEAR_F = "a further contract read straight off the nine-days-in-ten level's margin"
DH_MATURE = "the data hall at its type's established share"
DH_FULL = "the data hall at its agreed capacity"


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
    RC = F["route_choices"]
    sched, sd = F["r13_schedule"], F["r13_detail"]
    cust, cdt = F["r14_customer"], F["r14_detail"]
    fu = F["r12_further"]
    none_ = [n for n in call if fu[n] == "none"]
    some = [n for n in call if fu[n] != "none"]
    cf = RC[CAREFUL]
    held_c = [n for n in names if cf["verdicts"][names.index(n)].endswith("hold") and n in call]
    flex_c = [n for n in call if cf["further"][n] not in ("none", 0.0) and n not in some]
    md += ["## Final Recommendation", "",
           "**Commit reinforcement at %s for winter 2027/28 and hold %s: with each contract instructed in full on the "
           "design day the %s peaks stay under %s on nine days in ten against %s of firm capacity, and %s under %s MW "
           "against %s. More flexibility is no substitute at %s, where the load that comes back after the window caps what "
           "any further contract can do; %s would need %s MW more on its 2027/28 award's terms; %s's lowest peak comes from "
           "scheduling %s MW for the window and is still over firm capacity (%s MW on nine days in ten against %s); and %s "
           "would stay within firm capacity with a %s kVA %s energised on %s (%s MW against %s).** The careful but hurried "
           "reading is rejected: replaying the come-back as the megawatts the record's events showed (a mean of %s MW "
           "delivered at %s, where the design day delivers %s) holds %s at %s MW on nine days in ten and has %s held by %s MW "
           "more flexibility, and a straight line through the mornings reads Dunmore Street's 2025/26 design-day demand at "
           "%s MW where the mornings give %s."
           % (j(call), j(hold), {4: "four", 3: "three", 2: "two", 5: "five"}.get(len(call), str(len(call))),
              j("%s MW" % f1(q90[n]) for n in call), j("%s MW" % f1(Z[n]["firm"]) for n in call),
              j(hold), j(f1(q90[n]) for n in hold), j(f1(Z[n]["firm"]) for n in hold),
              j(none_), j(some), j(f1(fu[n]) for n in some), sd["primary"], f1(sched["schedule"]),
              f1(sched["one_in_ten"]), f1(sd["firm"]), cdt["primary"], "{:,}".format(cdt["kva"]), cdt["type"].lower(),
              cdt["energised"], f1(cust["one_in_ten"]), f1(cdt["firm"]),
              f1(Z[sd["primary"]]["event_mean_delivered"]), sd["primary"], f1(deliv[sd["primary"]]),
              j(held_c), j(f1(RF[CAREFUL][n]["one_in_ten"]) for n in held_c),
              j(flex_c), j(f1(cf["further"][n]) for n in flex_c),
              f1(car["R1"]["Dunmore Street"]), f1(d26["Dunmore Street"])), ""]

    md += ["## Supplementary Questions", "", "### %s" % XLSX, "",
           "1. Sheet Primaries holds one row per zone primary in name order (%s), with the constraint managed zone, the "
           "provider, the design-day demand in winter 2025/26, the megawatts the growth register's customers add, the "
           "design-day demand before flexibility in winter 2027/28, the megawatts contracted, the megawatts in service on "
           "%s, the share of them available on the design day, the megawatts delivered between 17:00 and 18:00, the "
           "half-hour of the day's peak, the expected peak, the level it stays under on nine design days in ten, firm "
           "capacity, the share of design days over firm capacity, Yes or No for reinforcement, and the further megawatts "
           "on the 2027/28 award's terms that would hold it within one design day in ten (No amount, a figure, or Not "
           "needed); megawatts to one decimal place and the share of days to the nearest whole per cent. Under the table a "
           "clustered column chart shows, for each primary, demand before flexibility, the expected peak, the "
           "nine-days-in-ten level and firm capacity. Sheet Flexibility carries the further contract's working for each "
           "primary to reinforce (the megawatts in service per megawatt of the 2027/28 step, what a further megawatt "
           "delivers, the lowest share any further contract reaches), %s's schedule and %s with the %s. Sheets Demand, "
           "Customers, Sites and Routes carry the rest: the cold end of each primary's demand, the customers behind each "
           "connections figure, the sites still to come by asset class, and what each shortcut would have committed."
           % (j(names), cv["assessment_date"], F["r13_detail"]["primary"], F["r14_detail"]["primary"],
              F["r14_detail"]["type"].lower()),
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
           "6. Share of design days over firm capacity (guideline 7: the day's demand, each provider's availability and the "
           "come-back varied together over the design days it requires, the estimates held at their central values; each "
           "share follows its primary's expected peak, so its range is the expected peak's range carried through): %s. "
           "Reinforce: %s; not %s."
           % ("; ".join("%s %d per cent (%s)" % (n, over[n], b0(B["R10"][n])) for n in names), j(call), j(hold)),
           "7. Further megawatts on the 2027/28 award's terms (the same kinds of site in the same proportions, planned for the "
           "same dates) that would hold each primary to reinforce within one design day in ten: %s. %s"
           % ("; ".join(("%s no amount" % n) if fu[n] == "none" else ("%s %s MW (%s)" % (n, f1(fu[n]), b1(B["R11"][n])))
                        for n in call),
              " ".join(("At %s the best any further contract does is %d per cent of design days over firm, at %s MW more."
                        % (n, F["r12_lowest"][n]["share_pct"], f1(F["r12_lowest"][n]["at_mw"])))
                       if F["r12_lowest"][n]["at_mw"] > 0 else
                       ("At %s every further megawatt only raises the peak after the window: it is lowest as awarded, %d per "
                        "cent of design days over firm." % (n, F["r12_lowest"][n]["share_pct"]))
                       for n in none_)),
           "8. %s scheduled short of its contract for the whole window, in the service terms' steps of 0.5 MW: %s MW (%s) "
           "gives the fewest design days over firm capacity, and nine days in ten its peak still reaches %s MW (%s) against "
           "%s, so no schedule keeps it within one design day in ten and its reinforcement stands."
           % (sd["primary"], f1(sched["schedule"]), b1(B["R12"]["schedule"]), f1(sched["one_in_ten"]),
              b1(B["R12"]["one_in_ten"]), f1(sd["firm"])),
           "9. %s with a %s kVA %s energised on %s: it adds %s MW (%s) to the evening peak by %s, and nine days in ten the "
           "peak stays under %s MW (%s) against %s, so %s stays within one design day in ten."
           % (cdt["primary"], "{:,}".format(cdt["kva"]), cdt["type"].lower(), cdt["energised"], f1(cust["adds"]),
              b1(B["R13"]["adds"]), cv["assessment_date"], f1(cust["one_in_ten"]), b1(B["R13"]["one_in_ten"]),
              f1(cdt["firm"]), cdt["primary"]),
           "", "### %s" % PPTX, "",
           "10. Six slides: the list to commit and the list to hold with each nine-days-in-ten level against firm capacity, "
           "and whether more flexibility could stand in; a clustered column chart of demand before flexibility, the expected "
           "peak, the nine-days-in-ten level and firm capacity for each primary, every bar carrying its value; the demand "
           "side (each primary's 2025/26 design-day demand, what the customers add and the 2027/28 figure); the flexibility "
           "side (megawatts contracted, in service and delivered for each primary); the alternatives (the further contract "
           "each primary to reinforce would need or that none would do, %s's schedule, %s with the %s); and the decision "
           "with each primary's share of design days over firm capacity."
           % (sd["primary"], cdt["primary"], cdt["type"].lower()),
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
              ("; carried to the design day's delivery (%s MW at %s, where the record's events delivered a mean of %s) this "
               "moves its peak to the half-hour ending %s." % (f1(deliv[late[0]]), late[0], f1(Z[late[0]]["event_mean_delivered"]),
                                                               Z[late[0]]["peak_hh"])) if late else "."),
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
        % (cv["design_day_degrees_below_zero"], f1(dz["coldest_without_service_2526"]), f1(RF[LINE]["Dunmore Street"]["demand_2526"]),
           dz["working_weekdays"], dz["at_or_below_freezing"], f2(ce["per_degree_above"]), f1(ce["knee_c"]),
           f2(ce["per_degree_below"]), each(d26)),
        "Customers (guideline 4: what the customers on `load_growth_register_2026-27.xlsx` will have added between the "
        "two assessment dates). Joined the register to `hh_customer_demand_monthly_2021-2026.csv` on the meter point, "
        "feeders to primaries through `network_feeders_11kv.xlsx`. A customer's demand as a share of its agreed capacity "
        "depends on its type and takes two to three years to build up, so each customer on supply was carried from its own "
        "latest months up its type's build-up to %s, and each customer still to connect was put on its type's. Counting "
        "only the customers due after the latest winter at their type's established share gives Charlecote Way %s MW and "
        "Hartwell Common %s; the register's customers add %s."
        % (cv["assessment_date"], f1(RF[MATURE]["Charlecote Way"]["connections"]), f1(RF[MATURE]["Hartwell Common"]["connections"]), each(conn)),
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
           f1(RF[PLANNED]["Fenwick Street"]["in_service"]), f1(insvc["Fenwick Street"]),
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
        "after it were read from the same events, each half-hour's come-back regressed on the megawatts delivered (%s of a "
        "megawatt back per megawatt delivered), and the design day rebuilt half-hour by half-hour. The come-back is in "
        "proportion to what the window delivered (Corvane Flex's %d events brought back %s and %s MW per MW delivered in the "
        "half-hour ending 20:00 on the smaller and the larger half of their deliveries, %s and %s MW in all), and the design "
        "day delivers far more than the record's events did: "
        "Ashcombe Road's events delivered a mean of %s MW and brought back %s MW in the half-hour ending 20:00, where its "
        "design day delivers %s and brings back %s. Replaying the record's megawatts would hold Ashcombe Road at %s MW on "
        "nine days in ten, and taking the delivery off the 17:00 to 18:00 peak at %s; rebuilt, its peak moves to the "
        "half-hour ending %s. Expected peaks: %s."
        % (j("%s %s" % (p, f2(back[p])) for p in provs), F["comeback_evidence"]["events"],
           f2(F["comeback_evidence"]["per_mw_small"]), f2(F["comeback_evidence"]["per_mw_large"]),
           f2(F["comeback_evidence"]["mw_small"]), f2(F["comeback_evidence"]["mw_large"]),
           f1(Z["Ashcombe Road"]["event_mean_delivered"]),
           f2(Z["Ashcombe Road"]["back_2000_record"]), f1(deliv["Ashcombe Road"]), f2(Z["Ashcombe Road"]["back_2000_design"]),
           f1(RF[FIXED]["Ashcombe Road"]["one_in_ten"]), f1(RF[NOREPLAY]["Ashcombe Road"]["one_in_ten"]),
           Z["Ashcombe Road"]["peak_hh"], each(peak)),
        "Nine design days in ten (guideline 7: the day's demand above or below its usual level by one proportion in every "
        "half-hour, each provider's available share from evening to evening and the come-back's own variation, as the "
        "mornings and the completed events show them; %s design days drawn, the estimates held at their central values). "
        "Each day's highest half-hour taken: %s. Share of design days over firm capacity: %s."
        % ("{:,}".format(cv["draws"]), "; ".join("%s %s MW against %s" % (n, f1(q90[n]), f1(Z[n]["firm"])) for n in names),
           "; ".join("%s %d per cent" % (n, over[n]) for n in names)),
        "Flexibility first. A further megawatt on the 2027/28 award's terms brings the award's own kinds of site on its "
        "planned dates, so it was given the in-service chance of the award's step, site by site: %s MW in service by %s "
        "per megawatt (Fenwick Street's step is %d per cent process load, which commissions late), times the share "
        "available. On the same design days each primary to reinforce was carried up through further contracts, the day "
        "replayed at each: %s. At %s each further megawatt delivered also comes back after the window, and the evening's "
        "peak climbs before the share reaches one day in ten. Read at the share of its contract the zone will have in "
        "service, Fenwick Street would need %s MW; read straight off the nine-days-in-ten margin, %s."
        % (j("%s %s" % (n, f2(F["r12_per_mw"][n])) for n in call), cv["assessment_date"],
           F["fenwick_process_pct"],
           "; ".join(("%s no amount (lowest share %d per cent)" % (n, F["r12_lowest"][n]["share_pct"])) if fu[n] == "none"
                     else ("%s %s MW" % (n, f1(fu[n]))) for n in call),
           j(none_), f1(RC[ZONE_RATIO]["further"]["Fenwick Street"]), f1(RC[LINEAR_F]["further"]["Fenwick Street"])),
        "%s's schedule. A schedule short of what is available is delivered as scheduled (the events that met their "
        "instruction show it), so a shorter schedule trades the window's peak against the come-back's and takes the "
        "provider's evening-to-evening spread out of the delivery: on the same design days, among the schedules the service "
        "terms allow (steps of 0.5 MW from 1.0 MW up to the contract), the fewest days over firm capacity come at %s MW, %s "
        "MW on nine days in ten against %s. Instructed in full it is %s; with the come-back read as the record's megawatts "
        "no schedule beats the contract in full."
        % (sd["primary"], f1(sched["schedule"]), f1(sched["one_in_ten"]), f1(sd["firm"]), f1(q90[sd["primary"]])),
        "%s with the %s. A %s kVA %s energised on %s is %s months old on %s; on its type's build-up (%s customers of the "
        "type in the settlement summary) it draws %d per cent of its type's established %s kW per kVA by then and adds %s "
        "MW: nine days in ten %s MW against %s. At its type's established share it would add %s MW and at its agreed "
        "capacity %s, and either would put %s over firm capacity."
        % (cdt["primary"], cdt["type"].lower(), "{:,}".format(cdt["kva"]), cdt["type"].lower(), cdt["energised"],
           F["customer_age_months"], cv["assessment_date"], F["customer_type_n"], cdt["build_up_pct"],
           f2(cdt["established_share"]), f1(cust["adds"]), f1(cust["one_in_ten"]), f1(cdt["firm"]),
           f1(RC[DH_MATURE]["customer_adds"]), f1(RC[DH_FULL]["customer_adds"]), cdt["primary"]),
        "Decision: reinforce %s; %s within firm capacity; only %s could be held instead by more flexibility."
        % (j(call), j(hold) + (" stays" if len(hold) == 1 else " stay"), j(some)),
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
           "record by class rules them out, read with the sites still to come and the sites withdrawn in it. Replaying the "
           "come-back as the record's megawatts would drop Ashcombe Road (%s MW) and offer Charlecote Way and Dunmore Street "
           "to more flexibility; the event days' own half-hours after the window, regressed on what each delivered, rule it "
           "out. Each of the %d variants of this assessment's own choices commits the same four, finds no further contract "
           "that would hold %s, and holds %s with the %s."
           % (f1(RF[LINE]["Dunmore Street"]["one_in_ten"]), f1(dz["firm"]), dz["at_or_below_freezing"],
              f1(RF[MATURE]["Charlecote Way"]["one_in_ten"]), f1(RF[MATURE]["Hartwell Common"]["one_in_ten"]),
              f1(RF[OBSERVED]["Charlecote Way"]["one_in_ten"]), f1(RF[OBSERVED]["Hartwell Common"]["one_in_ten"]),
              f1(RF["the megawatts contracted, at the share of megawatts in service"]["Fenwick Street"]["one_in_ten"]),
              f1(RF[PLANNED]["Fenwick Street"]["one_in_ten"]), f1(RF[POOLED]["Fenwick Street"]["one_in_ten"]),
              f1(RF[FIXED]["Ashcombe Road"]["one_in_ten"]), F["variants"]["n"], j(none_), cdt["primary"],
              cdt["type"].lower()), ""]
    open(path, "w").write("\n".join(md))
