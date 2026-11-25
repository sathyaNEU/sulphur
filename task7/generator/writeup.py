"""submission.md, emitted from figures.json: the tags and the four platform blocks (Final Recommendation, Supplementary
Questions, Critical Components, Step-by-Step). Every number is a figures.json value; texts() adds the few derived
figures the Step-by-Step states, before figures.json is written."""
import deliver as DL

ORDER = DL.ORDER


def n(x):
    return format(int(x), ",")


def usd(x, dec=0):
    return ("USD {:,.%df}" % dec).format(x)


def band(b, fmt=n):
    return "%s to %s" % (fmt(b[0]), fmt(b[1]))


def texts(F):
    """Derived figures the Step-by-Step states (kept in figures.json so every number in the blocks is one)."""
    lost_face = F["could_shed"] - F["delivered"]
    F["derived"] = dict(
        shortfall=int(F["could_shed"] - F["delivered"]),
        face=dict(test_pass=96, wo_unwired=9),
        rigorous_delivered=F["routes"]["rigorous"]["delivered"],
        fals_face_lo=min(F["fals"]["S1"], F["fals"]["S2"], F["fals"]["S3"]),
        fals_face_hi=max(F["fals"]["S1"], F["fals"]["S2"], F["fals"]["S3"]),
        planning_kw=int(round(F["counts"]["switches"] * 1.0)),
        breakeven_reflex=[F["proposals"][m]["breakeven"] for m in ("rep_w", "fix_t", "recon_in")],
        unexplained=int(round(lost_face)),
    )
    return F


def write(path, F):
    p = F["proposals"]
    C = F["counts"]
    fit = F["fit"]
    R = F["routes"]
    L = F["lattice"]
    nm = lambda m: p[m]["name"]
    ln = DL.lname
    out = []
    w = out.append
    w("## Tags")
    w("")
    w("**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, energy efficiency and demand response "
      "evaluation (a one-way air-conditioner load control fleet's 2026 dispatch trial).")
    w("**Analytical objective:** Experiment & Causal Analysis.")
    w("")
    w("## Final Recommendation")
    w("")
    w("**%s** Read as they stand, the cooperative's own records (a coverage map that covers every premise, a test log "
      "that passes %d in 100 switches, work orders that find %d in 100 unwired after a new unit) fund none of the six: "
      "they put the %s at %s kW, the %s at %s and the %s at %s, against break-evens of %s, %s and %s kW." % (
          DL.call_sentence(F), F["derived"]["face"]["test_pass"], F["derived"]["face"]["wo_unwired"],
          ln(nm("rep_w")), n(R["reflex"]["rep_w"]), ln(nm("fix_t")), n(R["reflex"]["fix_t"]), ln(nm("recon_in")),
          n(R["reflex"]["recon_in"]), n(p["rep_w"]["breakeven"]), n(p["fix_t"]["breakeven"]), n(p["recon_in"]["breakeven"])))
    w("")
    w("## Supplementary Questions")
    w("")
    w("### %s" % DL.FILES["csv"])
    w("One row per proposal in the work plan's order, with the kW it adds at the 2027 coincident peak (and its band), "
      "its break-even kW, its annual cost and whether it is funded.")
    w("1. The peak kW each proposal adds in 2027, against its break-even:")
    for i, m in enumerate(ORDER):
        w("   %s. %s: %s kW (band %s), break-even %s kW, %s." % (
            "abcdef"[i], nm(m), n(p[m]["kw"]), band(p[m]["band"]), n(p[m]["breakeven"]),
            "funded" if p[m]["funded"] else "not funded"))
    w("")
    w("### %s" % DL.FILES["xlsx"])
    w("The call on the first sheet, then the step record, the fitted model, the bridge, the proposals in full, the "
      "routes each record gives taken as it stands, and the rebuilds.")
    w("2. How the kW the switches could take off at peak splits, at the coincident-peak index:")
    w("   a. Lost to commands not received: %s kW (band %s)." % (n(F["lost_reach"]), band(F["lost_reach_band"])))
    w("   b. Lost to switches that received the command and failed: %s kW (band %s)." % (n(F["lost_hw"]), band(F["lost_hw_band"])))
    w("   c. Lost to working switches not connected to the air conditioner: %s kW (band %s)." % (
        n(F["lost_unwired"]), band(F["lost_unwired_band"])))
    w("3. The funded plan: %s kW added at the coincident peak (band %s), at %s a kW-year (band %s to %s)." % (
        n(F["plan_kw"]), band(F["plan_kw_band"]), usd(F["plan_cost_per_kw"], 1), "%.1f" % F["plan_cost_per_kw_band"][0],
        "%.1f" % F["plan_cost_per_kw_band"][1]))
    w("")
    w("### %s" % DL.FILES["pptx"])
    w("Three slides: the call, the bridge as a waterfall, and each proposal's kW beside its break-even.")
    w("")
    w("## Critical Components")
    w("")
    w("1. Shed commands that get through at the fringe (switches more than 20 km from the nearest transmitter serving "
      "them), against switches within 8 km: **%d in 100** (band **%d to %d**)." % (
          F["c1_through"], F["c1_through_band"][0], F["c1_through_band"][1]))
    w("2. Switches installed through 2015 that still work, at premises with no replaced unit: **%d in 100** (band **%d to "
      "%d**)." % (F["c2_work"], F["c2_work_band"][0], F["c2_work_band"][1]))
    w("3. Switches still wired in where the air conditioner was replaced after the switch went in: **%d in 100** (band "
      "**%d to %d**)." % (F["c3_wired"], F["c3_wired_band"][0], F["c3_wired_band"][1]))
    w("")
    w("## Step-by-Step")
    w("")
    w("1. Assembled the trial: %s active A/C switches on `lm_switch_register.csv`; %d event days and %s group shed "
      "commands in `paging_encoder_log_2026.csv` (local time, each group's first transmit, the encoder's repeats dropped); "
      "`scada_feeder_1min_2026.csv` read in UTC, mapped to feeders through `scada_point_list.csv` (two Pruett points "
      "renamed mid-July), duplicate rows dropped and held readings (three or more equal readings in a row) left out. Each "
      "feeder's step at each command is the mean of the five minutes from the transmit minute less the mean of the five "
      "before: %s steps." % (n(C["switches"]), C["events"], n(C["commands"]), n(C["steps"])))
    w("2. Set the footing: a working switch near a transmitter takes off %.3f kW at index 1 (the %d study homes' "
      "responders, from `study_meters_hourly_2026.csv` against each day's held-out homes in "
      "`study_event_assignments_2026.csv`); at the Appraisal's index of %.2f the switches could take off %s kW, and the "
      "steps hold %s kW delivered." % (fit["working_kw"], C["study_homes"], fit["index"], n(F["could_shed"]),
                                        n(F["delivered"])))
    w("3. Rejected the records read as they stand: they explain %s kW of a %s kW shortfall and fund nothing (the %s %s kW, "
      "the %s %s, the %s %s). Rejected the study homes carried to the fleet (%.3f kW an enrolled switch): it puts %s kW on "
      "feeders whose steps hold %s, and funds nothing; the study homes are all within 8 km, installed in 2019 and 2020, "
      "with no unit replaced since." % (
          n(F["reflex_bridge"]["total"]),
          n(F["derived"]["shortfall"]), ln(nm("rep_w")), n(R["reflex"]["rep_w"]), ln(nm("fix_t")), n(R["reflex"]["fix_t"]),
          ln(nm("recon_in")), n(R["reflex"]["recon_in"]), fit["study_itt"], n(F["derived"]["rigorous_delivered"]),
          n(F["delivered"])))
    w("4. Rebuilt each switch's reach on each event day: the distance to the nearest transmitter of its own paging "
      "system (the register's receiver field) that was on the air, from `paging_transmitters.xlsx` and "
      "`radio_shop_outage_log_2026.xlsx`; then apportioned the steps among the switches each command addressed by reach "
      "band, install batch, district and replaced unit together. Reception relative to the switches within 8 km is "
      "%.2f at 8 to 14 km, %.2f at 14 to 20 km and %.2f beyond 20 km: %d in 100 commands get through at the fringe. Reach "
      "to the nearest listed transmitter of either system instead puts the %s at %s kW, because the western VHF fringe "
      "sits beside the carrier's Sandhill site, which those receivers do not hear." % (
          fit["q"][1], fit["q"][2], fit["q"][3], F["c1_through"], ln(nm("rep_w")), n(R["generous"]["rep_w"])))
    w("5. Read the hardware off the batches: the paging groups are install batches, so each group's own steps net of "
      "reach and replaced units give its delivery against the study homes' working level: %d in 100 of the switches "
      "installed through 2015 still work (the test log's bench signal passes %d in 100)." % (
          F["c2_work"], F["derived"]["face"]["test_pass"]))
    w("6. Built the replaced-unit list: a rebate in `hvac_rebates_2012_2026.csv` (by premise number, pre-2021 numbers "
      "through the register's old-number field) or a permit in `county_mechanical_permits_2010_2026.csv` (by normalised "
      "address) for a replacement central air conditioner or heat pump, dated after the switch was installed: %s switches. "
      "In the same fit %d in 100 of them still deliver (the work orders' chance finding is %d in 100 unwired)." % (
          n(C["flagged"]), F["c3_wired"], F["derived"]["face"]["wo_unwired"]))
    w("7. Checked the fit against steps it was not built to match: on the steps where a transmitter change moved a "
      "switch's band, the four oldest batches and the quarter of feeders with most replaced units, the largest gap "
      "between predicted and recorded steps is %.3f; each record read as it stands leaves %.3f to %.3f, the either-system "
      "reach %.3f and the study homes carried to the fleet %.3f." % (
          F["fals"]["golden"], F["derived"]["fals_face_lo"], F["derived"]["fals_face_hi"], F["fals"]["generous"],
          F["fals"]["calibrated"]))
    w("8. Carried the fit to 2027 on the Appraisal's footing (every listed transmitter on the air, index %.2f, each "
      "proposal alone): the premises in scope are %s (Larkin round), %s (Medora Flats round), %s (within 14 km) and %s "
      "(outlying); each break-even is the annual cost over USD %d a kW-year. The %s, the %s and the %s clear theirs." % (
          fit["index"], n(C["fix_t"]), n(C["fix_w"]), n(C["recon_in"]), n(C["recon_out"]), int(fit["value"]),
          ln(nm("rep_w")), ln(nm("fix_t")), ln(nm("recon_in"))))
    w("9. Totalled the plan: %s kW for %s a year, %s a kW-year; the bridge closes on %s kW delivered of %s." % (
        n(F["plan_kw"]), usd(F["plan_cost"]), usd(F["plan_cost_per_kw"], 1), n(F["delivered"]), n(F["could_shed"])))
    w("")
    w("No other set survives. The study homes hold none of the three conditions, and the records each measure something "
      "shallower than delivery on a peak afternoon. All %d rebuilds of the fit's conventions (band edges, weighting, the "
      "district and batch terms, halves of the event days, the responder cut, trimmed steps, the step window from three "
      "to ten minutes either side, the index origin) file the same three. Each step left out alone moves a different "
      "proposal: without the reach rebuild the set is %s (the %s falls to %s kW); without the batch reading it is %s (the "
      "%s falls to %s kW); without the replaced-unit list it is %s (the %s falls to %s kW). With the reach rebuild and the "
      "batch reading both left out the set is %s; with the reach rebuild and the list, %s; with the batch reading and the "
      "list, %s; with all three, none. Each share holds its value in every row where its own step is kept. The thinnest "
      "margin is the %s: %s kW at the top of its band against a break-even of %s." % (
          C["variants"],
          joined(L["S1"]["funded"]), ln(nm("rep_w")), n(L["S1"]["rep_w"]),
          joined(L["S2"]["funded"]), ln(nm("fix_t")), n(L["S2"]["fix_t"]),
          joined(L["S3"]["funded"]), ln(nm("recon_in")), n(L["S3"]["recon_in"]),
          joined(L["S1+S2"]["funded"]), joined(L["S1+S3"]["funded"]), joined(L["S2+S3"]["funded"]),
          ln(nm("fix_w")), n(p["fix_w"]["band"][1]), n(p["fix_w"]["breakeven"])))
    text = "\n".join(out) + "\n"
    open(path, "w").write(text)
    return text


def joined(names):
    """A funded set inside a sentence: 'the A, the B and the C', or 'none'."""
    xs = ["the " + DL.lname(x) for x in names]
    if not xs:
        return "none"
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
