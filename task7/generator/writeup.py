"""task7 architecture 11: submission.md, the four answer blocks, every figure from figures.json at the precision the
golden deliverables print it (counts whole, Stagger's chance-weighted count to a tenth, kW to the hundredth, money to the
hundred dollars, the flip fee to the dollar), every band from the rivals run on the cut pack."""


def usd(v):
    return "$" + format(int(round(v)), ",")


def cnt(F, o):
    v = F[o]["over"]
    return ("%.1f" % v) if o == "stagger" else "%d" % v


def band(F, o):
    b = F["bands"][o]
    return ("%.1f and %.1f" % (b[0], b[1])) if o == "stagger" else "%d and %d" % (b[0], b[1])


def reps(x):
    return "%g replacement%s" % (x, "" if x == 1 else "s")


def write(F, path):
    o, s, q = F["own"], F["stagger"], F["sequence"]
    rc, rq = F["routes"]["careful"], F["routes"]["no_J3_perfect"]
    bt = F["band_totals"]
    L = ["## Tags", "",
         "**Domain:** Energy Systems & Utilities, energy efficiency and demand response evaluation (tariff and "
         "demand-response evaluation).",
         "**Analytical objective:** Experiment & Causal Analysis.", "",
         "## Final Recommendation", ""]
    L.append("**Make Quillpoint Sequence the EV Overnight rate's charging default for 2027 and carry %d transformer "
             "replacements (%s) in the 2027 work plan**: at %s for the year it costs less than Quillpoint Stagger (%s) or "
             "the members' own schedules (%s). This rejects Stagger, which the pilot's average managed night shows "
             "clearing every transformer (%g over, %s), because a random start still lets the few chargers on a small "
             "transformer land together on some night of the summer: replayed night by night, Stagger leaves %s over."
             % (q["over"], usd(q["replace"]), usd(q["total"]), usd(s["total"]), usd(o["total"]),
                rc["stagger"], usd(rc["total"]), cnt(F, "stagger")))
    L += ["", "## Supplementary Questions", "", "### ev_overnight_default_2027_memo.docx", ""]
    L.append("1. The call, in the memo's title and first paragraph: Quillpoint Sequence as the 2027 default, with %d "
             "transformer replacements in the 2027 work plan (between %d and %d) costing %s." %
             (q["over"], F["bands"]["sequence"][0], F["bands"]["sequence"][1], usd(q["replace"])))
    L.append("2. Transformers serving the rate's chargers that each option leaves over their limit in a summer like 2026: "
             "members' own schedules %d (between %s), Quillpoint Stagger %s with each transformer at its chance of being "
             "over (between %s), Quillpoint Sequence %d (between %s)." %
             (o["over"], band(F, "own"), cnt(F, "stagger"), band(F, "stagger"), q["over"], band(F, "sequence")))
    L.append("3. The platform's fee for the %s enrolled chargers for 2027: own schedules $0, Stagger %s ($%g a charger), "
             "Sequence %s ($%g a charger)." % (format(F["n_chargers"], ","), usd(s["fee"]), F["fee_rate"]["stagger"],
                                                  usd(q["fee"]), F["fee_rate"]["sequence"]))
    L.append("4. What the replacements would cost at DPS-7's installed costs: own schedules %s, Stagger %s, Sequence %s "
             "(each within the spread of its count)." % (usd(o["replace"]), usd(s["replace"]), usd(q["replace"])))
    L.append("5. The total for 2027: own schedules %s (between %s and %s), Stagger %s (between %s and %s), Sequence %s "
             "(between %s and %s)." % (usd(o["total"]), usd(bt["own"][0]), usd(bt["own"][1]), usd(s["total"]),
                                         usd(bt["stagger"][0]), usd(bt["stagger"][1]), usd(q["total"]),
                                         usd(bt["sequence"][0]), usd(bt["sequence"][1])))
    L.append("6. The pilot's managed charging took %.2f kW per enrolled charger off the 23:00 to 23:15 interval in July "
             "and August 2026 (within 0.1 kW): %.2f kW in the managed quarter against %.2f kW on the owners' own "
             "schedules." % (abs(F["pilot_effect"]), F["pilot_managed"], F["pilot_own"]))
    L.append("7. Chargers enrolled on the rate on 1 November 2026: %s." % format(F["n_chargers"], ","))
    L.append("8. The call changes if Sequence's fee rises above about $%d per charger for the year (between $%d and $%d), "
             "where Stagger would cost the same." % (F["flip_fee"], F["band_flip"][0], F["band_flip"][1]))
    L.append("9. A chart of the transformers over their limit under each option, stacked by transformer size.")
    L += ["", "### ev_overnight_transformers_2027.csv", ""]
    L.append("10. %d rows, one for each transformer serving an enrolled charger, with its location, substation, kVA, "
             "15-minute limit in kW, homes, enrolled chargers, and its summer peak in kW under each option: own schedules "
             "(%d marked over), Stagger (its mean peak and its chance of being over, the chances summing to %s) and "
             "Sequence (%d marked over), with the replacement cost." % (F["n_tx"], o["over"], cnt(F, "stagger"), q["over"]))
    L += ["", "## Critical Components", ""]
    L.append("1. Quillpoint Stagger leaves **%s** transformers over their limit (between %s), not the **%g** the pilot's "
             "average managed night suggests." % (cnt(F, "stagger"), band(F, "stagger"), rc["stagger"]))
    L.append("2. Quillpoint Sequence leaves **%d** transformers over (between %s): its rule has to start a late charger "
             "alongside others on heavy nights, where one charger at a time would leave **%g**." %
             (q["over"], band(F, "sequence"), rq["sequence"]))
    L.append("3. The members' own schedules leave **%d** transformers over (between %s), not the **%g** the 2026 meters "
             "show with a quarter of the chargers under Stagger." % (o["over"], band(F, "own"), rc["own"]))
    L.append("4. The pilot's managed charging took **%.2f kW** per enrolled charger off 23:00 to 23:15." % abs(F["pilot_effect"]))
    L += ["", "## Step-by-Step", ""]
    L.append("1. From `ev_overnight_roster_2026-11-02.csv`, with the re-imported rows dropped, each swapped charger "
             "followed to its replacement and the closed ones left out: %s chargers enrolled on 1 November 2026." %
             format(F["n_chargers"], ","))
    L.append("2. Through `gis_service_points_2026-10-30.csv`, the transfers in `distribution_work_orders_2025_2026.xlsx` "
             "and `ami_meter_exchanges_2026.csv`, they sit on %d transformers; each one's nameplate is the register's as "
             "corrected by the change-outs (DPS-7 section 4)." % F["n_tx"])
    L.append("3. Each transformer's base is its homes' hourly reads (the three `mdm_hourly_` files, re-sent rows dropped) "
             "less the enrolled chargers' charging from `quillpoint_sessions_2024-06_2026-09.csv`, put from UTC onto "
             "local time.")
    L.append("4. The pilot's randomised comparison (`pilot_assignment_2025.csv`): the managed quarter charged %.2f kW per "
             "enrolled charger at 23:00 to 23:15 against %.2f on own schedules. Carried to the transformers as the managed "
             "quarter's average night times their chargers, it puts Stagger at %g transformers over, the shallow read." %
             (F["pilot_managed"], F["pilot_own"], rc["stagger"]))
    L.append("5. The limit is each transformer's single highest quarter-hour of the summer (DPS-7 2.1), so Stagger is "
             "replayed night by night on every charger's 2026 sessions with its random start drawn %s times: the few "
             "chargers on a small transformer still coincide on some nights, and Stagger leaves %s over at their chance "
             "(EV-4 4.3)." % (format(400, ","), cnt(F, "stagger")))
    L.append("6. Sequence, never piloted, is run by its rule in `quillpoint_proposal_2027.xlsx` on each night's plug-ins, "
             "energy and unplug times: on heavy nights a late charger starts alongside, and %d transformers stay over, "
             "where one charger at a time would leave %g." % (q["over"], rq["sequence"]))
    L.append("7. Own schedules are rebuilt for every charger (its own-schedule sessions, the managed quarter's from summer "
             "2024, or the usual charging the member gave at enrolment): %d over, where the 2026 loads as metered give %g."
             % (o["over"], rc["own"]))
    L.append("8. Every option's base is lifted from the hourly reads to the quarter-hour by the highest quarter-hour above "
             "each hour on the %d monitored transformers (`transformer_monitors_15min_2026-07_08.csv`), scaled by the "
             "square root of a transformer's homes." % F["monitors"])
    L.append("9. At DPS-7's installed costs and Quillpoint's fees, Sequence costs %s, Stagger %s and own schedules %s; "
             "Sequence stays cheapest until its fee passes about $%d a charger." %
             (usd(q["total"]), usd(s["total"]), usd(o["total"]), F["flip_fee"]))
    L += [""]
    L.append("No other conclusion survives. The pilot's average night prices a coincidence it cannot see, so it files "
             "Stagger with nothing to replace; taking Sequence as the pilot's managed quarter files Stagger again, and "
             "taking it as one charger at a time files Sequence with %s, where its own rule leaves %d. The 2026 "
             "meters are not the members' own schedules, and every replay that lifts the hourly reads to the quarter-hour "
             "another way (the monitored transformers' peaks, or none at all) still calls Sequence." % (reps(rq["sequence"]), q["over"]))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
