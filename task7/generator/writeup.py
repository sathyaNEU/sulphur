"""The memo's text, the workbook's method notes and submission.md, every figure from figures.json."""


def mwh(x):
    return format(int(round(x)), ",")


def usd(x):
    return "$" + format(int(round(x, -2)), ",")


def texts(F):
    fund = sorted(F["funded"])
    care = sorted(F["routes"]["the careful route (the reflex route)"])
    F["memo_head"] = [F["org"] + ", System Planning",
                      "To: Joseph Harmon, manager of distribution engineering    From: Mary Wilson, system planning    Date: 20 November 2026"]
    F["memo_title"] = "Voltage optimization in 2027: %d feeders, %s" % (len(fund), usd(F["total_cost"]))
    F["memo_call"] = ("Put voltage optimization on %s in the 2027 capital program. Under VO-1 each of them saves more "
                      "energy at its substation breaker over a year like 2026 than its equipment costs: together %s MWh a "
                      "year for %s installed. The other %d feeders do not clear their cost." %
                      (", ".join(fund), mwh(F["total_save_mwh"]), usd(F["total_cost"]), len(F["ids"]) - len(fund)))
    F["memo_body"] = [
        ("What the trial measured", "On the eight trial feeders the energy drawn fell by %.2f percent on average (%s, feeder by "
         "feeder) for each 1 percent the regulators actually took off the feeder-head voltage. The ON days did not all run: "
         "on some the pilot regulators stayed in local mode, and each ON day ramped down over its first hour." %
         (F["trial_mean"], ", ".join("%.2f" % F["trial_effect"][i] for i in F["trial"]))),
        ("Carrying it to every feeder and every hour", "The trial ran in spring and autumn on eight feeders. Water heaters and "
         "resistive heat draw less at a lower voltage only until their thermostats keep them on longer, so over a day they "
         "give their energy back; every other load answers in proportion to its share. Each feeder's share of thermostatic "
         "load hour by hour comes from its own load against the weather, the 2025 appliance survey and the 2024 load "
         "research; scaled to what the trial measured, that gives each feeder's response through the whole year, from %.2f "
         "to %.2f percent per 1 percent, lowest where resistive heat is common." % (F["cvrf_lo"], F["cvrf_hi"])),
        ("How far each feeder can go", "VO-1 keeps every customer at or above 115 V in every hour. The far-end meters set what "
         "each feeder can give hour by hour: the trial's 4.8 V on the short, lightly loaded feeders, much less at the far end "
         "of the long rural lines and on the heaviest summer and winter hours."),
        ("Losses", "Lowering the voltage raises the current the constant-power loads draw, so on %d of the 24 feeders the "
         "lines' own losses rise and give back part of the customers' saving, by up to %s MWh a year; current squared, "
         "fitted on the feeders with substation revenue meters, sets the change. The annual report's 6.1 percent loss rate, "
         "added in proportion, gets the sign wrong." % (F["n_loss_rise"], mwh(F["largest_loss_rise_mwh"]))),
        ("What a quicker reading would fund", "Carrying the trial feeders' average response to the rest, flat through the "
         "year, and adding 6.1 percent for losses funds %s instead." % ", ".join(care)),
    ]
    F["method"] = [
        "Customer energy: the meter data management system's feeder interval sums, the October re-sent rows dropped.",
        "Trial: each trial feeder's daily customer energy over its same-class untested feeders' on the same day, on the trial "
        "days, regressed on the day's achieved feeder-head reduction (bus SCADA less the pilot regulator's output) with "
        "heating, cooling and day-type terms.",
        "Makeup: each feeder's quarter-hour load regressed on its quarter-of-day by day-type profile with heating and cooling "
        "degrees; heating split between resistive heat and heat pumps by the survey's holdings at the 2024 load research's "
        "draws; water heating at the load research's yearly use a heater of the survey's holding.",
        "Response: thermostatic load gives its energy back; every other load answers in proportion to its share, scaled to "
        "the trial's measured response (the median over the trial feeders of trial response over non-thermostatic share).",
        "Volts: hour by hour, the far-end meters' lowest reading less 115 V, at most 4.8 V; the trial's ON days restored "
        "to normal running.",
        "Losses: head-meter energy less customer energy against current squared times the register's ohms, fitted on the "
        "head-metered feeders; applied at each feeder's load and voltage with and without VO.",
        "Value: yearly MWh at the substation times USD 48 times 9.4 (VO-1 2.4), against the 2027 capital plan's estimate.",
    ]
    return F


def write(path, F, bands):
    ids = F["ids"]
    fund = sorted(F["funded"])
    care = sorted(F["routes"]["the careful route (the reflex route)"])
    b = bands

    def per(key, bkey, fmt):
        return "; ".join(("%s " + fmt + " (" + fmt + " to " + fmt + ")") % (i, F[key][i], b[bkey][i][0], b[bkey][i][1]) for i in ids)
    L = ["# task7: Platte Ridge PPD, voltage optimization in the 2027 capital program", "", "## Tags", "",
         "**Domain:** Energy Systems & Utilities (Energy efficiency & demand response evaluation).",
         "**Analytical objective:** Experiment & Causal Analysis.", "", "## Final Recommendation", "",
         "Put voltage optimization on %s in the 2027 capital program (%s installed, %s MWh a year saved at the substation): "
         "each saves more energy at its breaker over a year like 2026 than its equipment costs under VO-1. Not the careful "
         "reading that carries the trial feeders' average response to every feeder flat through the year and adds the annual "
         "report's 6.1 percent for losses, which funds %s." %
         (", ".join(fund), usd(F["total_cost"]), mwh(F["total_save_mwh"]), ", ".join(care)), "",
         "## Supplementary Questions", "", "### vo_program_2027.xlsx", ""]
    items = [
        "Sheet Decision: one row per feeder with its yearly saving at the customer meters, the rise in its own line losses, "
        "its yearly saving at the substation, the saving's present value, its installed cost, the ratio and the decision; "
        "sheets Trial and Feeders carry the figures below.",
        "The feeders that receive VO in 2027 (exact): %s." % ", ".join(fund),
        "The 2027 program's total yearly saving at the substation, MWh: %s (%s to %s), for %s installed." %
        (mwh(F["total_save_mwh"]), mwh(b["total"][0]), mwh(b["total"][1]), usd(F["total_cost"])),
        "Each feeder's expected yearly energy saving at the substation, MWh (band in brackets): " + per("save_mwh", "save", "%.0f") + ".",
        "Each feeder's expected yearly energy saving at the customer meters, MWh (band in brackets): " + per("cust_mwh", "cust", "%.0f") + ".",
        "The rise in each feeder's own line losses under VO, MWh a year, negative where they fall (band in brackets): " +
        per("loss_mwh", "loss", "%.0f") + ".",
        "Each feeder's yearly change in customer energy per 1 percent of voltage removed, percent (band in brackets): " +
        per("cvrf", "cvrf", "%.2f") + ".",
        "Each feeder's 2026 energy at the customer meters, MWh (within 0.5 percent): " +
        "; ".join("%s %s" % (i, mwh(F["energy_mwh"][i])) for i in ids) + ".",
        "The average reduction in volts the equipment could hold each feeder at over the year, 120 V base (band in brackets): " +
        per("room_v", "room", "%.2f") + ".",
        "The trial's change in energy per 1 percent of voltage removed, averaged over the eight trial feeders, percent: "
        "%.2f (%.2f to %.2f); sheet Trial also shows each trial feeder's own figure." % (F["trial_mean"], b["trial_mean"][0], b["trial_mean"][1]),
    ]
    q = 0
    for s in items:
        q += 1
        L.append("%d. %s" % (q, s))
    L += ["", "### vo_program_2027_memo.docx", ""]
    q += 1
    L.append("%d. A short memo that opens on the decision, lists the funded feeders with their saving and cost, shows each "
             "feeder's value over cost, and says what the trial measured and how it was carried to every feeder and hour." % q)
    L += ["", "## Critical Components", ""]
    top = sorted(ids, key=lambda i: abs(F["value_ratio"][i] - 1))[:3]
    L.append("1. The yearly saving at the substation on the feeders nearest the line (forecasting): %s." %
             "; ".join("%s **%s MWh** against a break-even of %s MWh" % (i, mwh(F["save_mwh"][i]), mwh(F["break_even_mwh"][i])) for i in top))
    lo = sorted(ids, key=lambda i: F["cvrf"][i])[:3]
    hi = sorted(ids, key=lambda i: -F["cvrf"][i])[:2]
    L.append("2. Each feeder's own yearly response, not the trial's %.2f carried flat (modeling): %s at the low end, %s at the high end." %
             (F["trial_mean"], "; ".join("%s **%.2f**" % (i, F["cvrf"][i]) for i in lo), "; ".join("%s **%.2f**" % (i, F["cvrf"][i]) for i in hi)))
    up = sorted(ids, key=lambda i: -F["loss_mwh"][i])[:3]
    L.append("3. The losses that rise under VO (decomposition): %s MWh a year, against the fall the report's 6.1 percent implies." %
             "; ".join("%s **+%s**" % (i, mwh(F["loss_mwh"][i])) for i in up))
    L += ["", "## Step-by-Step", ""]
    steps = [
        "Assemble the customer energy from mdm_feeder_interval_kwh_2026.csv (the October re-sent rows dropped) and the register's "
        "feeders, substations and classes.",
        "Read the trial: the regulator log against the bus SCADA gives the voltage each pilot regulator actually took off each "
        "day; some ON days stayed in local mode and each ramped down over its first hour. Regress each trial feeder's daily "
        "energy, over its same-class untested feeders', on that achieved reduction with weather and day-type terms: %.2f percent "
        "per 1 percent on average (%.2f on the day's assignment)." % (F["trial_mean"], F["trial_mean_assigned"]),
        "Build each feeder's makeup: its load against its quarter-of-day profile and heating and cooling degrees, the heating "
        "split by the survey between resistive heat and heat pumps at the load research's draws, water heating at the "
        "survey's holding and the load research's yearly use a heater. Thermostatic load gives its energy back over the day, "
        "so the response is the non-thermostatic share times the trial's measured response per unit of that share, hour by "
        "hour through the year: %.2f to %.2f percent per 1 percent over the year, where the hurried reading carries %.2f to "
        "every feeder." % (F["cvrf_lo"], F["cvrf_hi"], F["trial_mean"]),
        "Set the volts each feeder can give from its far-end meters, hour by hour, to keep 115 V, at most 4.8 V, as VO-1 sets it, "
        "the trial's ON days restored: averages from %.2f to %.2f V." % (min(F["room_v"].values()), max(F["room_v"].values())),
        "Fit the losses on the head-metered feeders against current squared and apply them with and without VO: losses rise "
        "on %d feeders, by up to %s MWh a year." % (F["n_loss_rise"], mwh(F["largest_loss_rise_mwh"])),
        "Value each feeder's yearly saving at the substation at USD 48 and 9.4 against its capital-plan cost: %s clear it." % ", ".join(fund),
        "The shortcuts land elsewhere: %s." % "; ".join("%s funds %s" % (k, ", ".join(sorted(v))) for k, v in F["routes"].items()),
    ]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s" % (i, s))
    L += ["", "No other conclusion survives the records: an untested feeder answers as its own makeup does, not as the trial "
          "feeders' average; thermostatic load gives its energy back, so winter is worth less where resistive heat is common; "
          "and the lines' losses rise with the current the constant-power loads draw. Every heating ratio, weather form, trial "
          "control, trial scale and loss fit in the golden family, and every input moved by its spread, funds the same feeders.", ""]
    open(path, "w").write("\n".join(L))
