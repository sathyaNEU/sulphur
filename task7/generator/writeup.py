"""task7 architecture 10: submission.md, the four answer blocks, every figure from figures.json at the precision the
golden deliverables print it (kW to the thousandth, shares in whole per cent, devices whole, money to the dollar, the
totals' dollars to the hundred, MW to the hundredth), every band from the generator's own conventions."""


def n(v):
    return format(int(round(v)), ",")


def usd(v):
    return "$" + format(int(round(v)), ",")


def pct(v):
    return "%d%%" % int(round(100 * v))


def write(F, path):
    ps = F["providers"]
    kw, bar = F["kw"], F["bar_kw"]
    care = F["care_kw"]
    cv = F["conventions"]
    keep = F["renewed"]
    drop = [p for p in ps if p not in keep]
    L = ["## Tags", "",
         "**Domain:** Energy Systems & Utilities, energy efficiency and demand response evaluation.",
         "**Analytical objective:** Experiment & Causal Analysis.", "",
         "## Final Recommendation", ""]
    L.append("**Renew %s and %s for summer 2027; do not renew %s or %s.** Kitebrook's 2027 devices take %.3f kW each off "
             "our load in the 4CP intervals against the %.3f kW its price needs, Lumivale's %.3f against %.3f and Pinecrest "
             "Home's %.3f against %.3f. This rejects reading the test events' own reduction at the 4CP intervals, which "
             "renews Lumivale (%.3f kW) and Pinecrest Home (%.3f kW) and drops Kitebrook (%.3f kW): the 4CP days come late "
             "in heat waves, when members leave events; Pinecrest Home's 2027 fleet is mostly retail-rebate devices; and "
             "Kitebrook's homes are larger and older than the research sample's."
             % (", ".join(keep[:-1]), keep[-1], ", ".join(drop[:-1]), drop[-1], kw["Kitebrook"], bar["Kitebrook"],
                kw["Lumivale"], bar["Lumivale"], kw["Pinecrest Home"], bar["Pinecrest Home"], care["Lumivale"],
                care["Pinecrest Home"], care["Kitebrook"]))
    L += ["", "## Supplementary Questions", "", "### provider_renewals_2027_workbook.xlsx", ""]
    L.append("1. Sheet 'providers', each provider's kW per device enrolled on 1 July 2027 taken off the co-op's load in the "
             "4CP intervals of a summer like 2024 to 2026, each within the kW given beside it (the spread of the "
             "defensible methods): %s. Sheet '4CP intervals' gives each of the %d intervals, the %s "
             "interval at nothing for every provider (no alert was called)."
             % (", ".join("%s %.3f (within %.3f)" % (p, kw[p], F["kw_band"][p]) for p in ps), cv["intervals"],
                " and ".join(F["missed_cp"])))
    L.append("2. Sheets 'providers' and '2027 fleets', each provider's devices enrolled on 1 July 2027 and what its quote "
             "would cost (each within %d per cent): %s." % (cv["n_band_pct"], "; ".join(
                 "%s %s devices, %s" % (p, n(F["n27"][p]), usd(F["cost"][p])) for p in ps)))
    L.append("3. Sheet 'providers', the renewed providers (%s) in all: %.2f MW off the co-op's 4CP load, saving %s of "
             "transmission cost, %s net of the %s their quotes cost (each within %d per cent)."
             % (", ".join(keep), F["mw"], usd(F["saving_usd"]), usd(F["net_usd"]), usd(F["paid_usd"]), cv["total_band_pct"]))
    L += ["", "### provider_renewals_2027_memo.docx", ""]
    L.append("4. A memo of about a page for the board: the call first, a table of each provider's kW per 2027 device "
             "against the kW its price needs, its devices, its quote's cost and the verdict, a chart of the six against "
             "their lines, and short paragraphs on why the test events overstate Lumivale and Pinecrest Home and "
             "understate Kitebrook, and on Ondera's window.")
    L += ["", "## Critical Components", ""]
    L.append("1. On the 4CP days **%s** of Lumivale's enrolled devices were still in its event at the middle of the 4CP "
             "interval (between %d%% at its end and %d%% at its start; the band runs 2 points beyond both), against "
             "**%s** of its called devices on the test events at 17:30 (within 3 points)."
             % ("%d%%" % F["pct"]["lumivale_cp"], min(F["pct"]["lumivale_cp_start"], F["pct"]["lumivale_cp_end"]),
                max(F["pct"]["lumivale_cp_start"], F["pct"]["lumivale_cp_end"]), "%d%%" % F["pct"]["lumivale_test"]))
    L.append("2. Pinecrest Home's 2027 fleet is **%s** retail-rebate devices and keeps **%s** of its devices in the event "
             "at the 4CP intervals, against **%s** of today's fleet on the 4CP days (each within 3 points)."
             % ("%d%%" % F["pct"]["pinecrest_retail27"], "%d%%" % F["pct"]["pinecrest_2027"],
                "%d%%" % F["pct"]["pinecrest_now"]))
    L.append("3. Kitebrook's 2027 fleet sheds **%.2f** times what its research-sample devices shed, by the homes' cooling "
             "slopes from living area and year built (within 0.06)." % F["transport"]["Kitebrook"])
    L.append("4. Ondera's event ends at %s, before **%d** of the twelve 4CP intervals, so its devices add load there: "
             "**%.3f** kW per device." % (F["window_end"]["Ondera"], F["after_window"]["Ondera"], kw["Ondera"]))
    L += ["", "## Step-by-Step", ""]
    s = 1
    L.append("%d. Put the six providers' reports on one footing (`corvane_event_report_2024_2026.csv` and "
             "`kitebrook_events_2024_2026.csv` on UTC, the rest local; Corvane, Lumivale and Ardena list unreached devices, "
             "Ondera, Kitebrook and Pinecrest Home leave them out) and keyed each row to its programme id through "
             "`peak_partners_roster_2026-10-30.csv`, swapped thermostats included; mapped the research sample's meters "
             "through `member_accounts_2026.csv`, exchanges included." % s)
    s += 1
    L.append("%d. Measured each provider's reduction on the 24 randomised test events "
             "(`mv_event_assignments_2024_2026.csv`, `ami_15min_reads_peak_partners_2024_2026.csv`): held-back half against "
             "called half, 15 minutes at a time, each home's own 13:00 to 14:30 load that day as the covariate." % s)
    s += 1
    L.append("%d. Split the reduction into the shed of a device still in the event (a straight line in the interval's "
             "temperature, `weather_kcdr_hourly_2024_2026.csv`) and the share still in it, every enrolled device in the "
             "denominator." % s)
    s += 1
    L.append("%d. Read the share on the 4CP days themselves (`ercot_4cp_intervals_2016_2026.csv` against "
             "`peak_partners_event_log_2024_2026.xlsx`): each 4CP day is the %s or later alert day of a heat wave, and "
             "Lumivale keeps %s at the 4CP interval against %s on the test events. The hurried reading takes the test "
             "events' reduction straight to the 4CP intervals." % (s, {2: "second", 3: "third", 4: "fourth"}[F["cp_run_min"]],
                                                                    "%d%%" % F["pct"]["lumivale_cp"],
                                                                    "%d%%" % F["pct"]["lumivale_test"]))
    s += 1
    L.append("%d. Carried each fleet to 1 July 2027 (the devices enrolled now, each at its channel's leaving rate since "
             "2021, and the quotes' new enrolments (`provider_quotes_summer_2027.xlsx`) like the provider's recent enrolments through "
             "the same channel); the share in the event modelled device by device on the 4CP days (the day, the channel, "
             "the years enrolled) and taken for the 2027 fleet. Pinecrest Home's fleet becomes %s retail and keeps %s in "
             "the event." % (s, "%d%%" % F["pct"]["pinecrest_retail27"], "%d%%" % F["pct"]["pinecrest_2027"]))
    s += 1
    L.append("%d. Carried the shed to each fleet's homes: each research-sample home's cooling slope off its quiet days, "
             "predicted for every home from living area and year built in `calder_cad_residential_2026.csv` matched by "
             "address (county roads and FM roads in two forms); Kitebrook's fleet sheds %.2f times its sample devices'."
             % (s, F["transport"]["Kitebrook"]))
    s += 1
    L.append("%d. Read each provider at each 4CP interval's place in its window (Ondera's after its %s end), "
             "%s at nothing, and averaged the twelve: %s." % (s, F["window_end"]["Ondera"], " and ".join(F["missed_cp"]),
                                                             ", ".join("%s %.3f" % (p, kw[p]) for p in ps)))
    s += 1
    L.append("%d. Set each against the kW its quoted price needs at $%.2f per kW "
             "(`board_policy_412_demand_response_providers.pdf`, `transmission_charge_notice_2027.pdf`): %s clear it; "
             "%s do not." % (s, F["rate"], ", ".join(keep),
                                                                                ", ".join(drop)))
    s += 1
    L.append("%d. The renewed providers' %s devices take %.2f MW off the 4CP load and save %s, %s net of their quotes."
             % (s, n(F["renewed_devices"]), F["mw"], usd(F["saving_usd"]), usd(F["net_usd"])))
    L.append("")
    L.append("No other conclusion survives. Reading the test events' reduction at the 4CP intervals renews Lumivale and "
             "Pinecrest Home and drops Kitebrook, but the 4CP days' own reports show Lumivale's members leaving its long, "
             "deep event late in a heat wave, the quotes and the roster put Pinecrest Home's 2027 fleet in the retail "
             "channel that is often offline and leaves events, and the appraisal roll puts Kitebrook's fleet in homes "
             "that shed far more than the research sample's. Each correction alone moves its own provider across its line, "
             "and every defensible variant of each (a linear home model, one leaving rate for every channel, the test "
             "halves compared without the pre-event load) keeps the same three renewed.")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
