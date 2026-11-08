"""submission.md, drafted from figures.json and nothing else."""
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
SEASON_M = ("April", "May", "June", "July", "August", "September", "October")
PAC_M = ("May", "June", "July", "August")


def fmt(n):
    return "{:,}".format(int(n))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    per = F["per_sub"]
    loads = F["loads_kg"]
    lm = F["loads_month_kg"]
    pac = F["pac_lb"]
    bsm = F["days_by_sub_month"]
    spared = F["carbon_spared_lb"]
    others = [k for k in per if k != F["call"]]
    sf = dt.date.fromisoformat(F["strat_first"])
    sl = dt.date.fromisoformat(F["strat_last"])
    off = F["dun_offsets_ft"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences, pollution source attribution.  ")
    L.append("**Analytical objective:** Root-Cause Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Place the 2027 atrazine cost-share program in the %s sub-watershed.** %s's atrazine was behind all %d of "
             "the 2026 season's days on which the raw water was above the 3.0 ug/L trigger, and no other "
             "sub-watershed's was behind any. Not the Tessel River, which carried the most atrazine past its station "
             "in every month from April to July but whose warm water spread over the stratified lake's surface layer, "
             "above the intake; not Oxley or Dunmore Creek, whose water also entered above the intake's layer; not "
             "Ladd Branch, whose water ran to the bottom.\n" % (F["call"], F["call"], F["call_days"]))
    L.append("## 2. Critical Components\n")
    L.append("1. Days in the 15 April to 31 October season with the raw-water result above 3.0 ug/L: **%d**."
             % F["days_total"])
    L.append("2. The lake was stratified at the dam from **%s** to **%s**, and on every day above the trigger %s was "
             "the only sub-watershed whose water had entered the lake within the intake's layer." %
             (sf.strftime("%-d %B"), sl.strftime("%-d %B"), F["call"]))
    L.append("3. Days above the trigger each sub-watershed's atrazine caused: %s **%d**; %s.\n"
             % (F["call"], F["call_days"], "; ".join("%s **%d**" % (k, per[k]) for k in others)))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took each day's raw-water result from raw_water_log_2026-01-01_to_2026-05-26.csv and "
             "LIMS_raw_water_2026-05-20_to_2026-10-31.xlsx as SOP-WQ-07 2.3 sets it (the GC/MS confirmation where "
             "one was run, otherwise the ELISA screen) and counted the season's days above 3.0 ug/L (plan 5.2): %d."
             % F["days_total"])
    L.append("2. Built the lake's daily mean temperature profile from MERRIN_BUOY_Hourly_2026.dat (logger clock on CST; "
             "sensor depths from buoy_service_log_2026.csv, 0.5 to 15.5 m before the 10 June re-hang and 1 to 16 m "
             "after) and the intake's daily depth below the surface from the pool elevation in "
             "merrin_dam_daily_log_2026.xlsx (NGVD29) less the intake centreline on intake_tower_record_drawing_S-4.pdf "
             "(829.24 ft NAVD88, NGVD29 plus 0.24 ft): stratified from %s to %s, the intake %.1f to %.1f m down in "
             "June and July." % (sf.strftime("%-d %B"), sl.strftime("%-d %B"), F["intake_depth_m"][0],
                                 F["intake_depth_m"][1]))
    L.append("3. Placed each tributary's water each day at the depth where that day's profile was as warm as the "
             "tributary's daily mean temperature (TR-01, FC-02 and OC-03 exports on local time; the DC-04 and LB-05 "
             "loggers on UTC), and on each day above the trigger listed the sub-watersheds whose water had entered "
             "within two metres of the intake's depth since the lake stratified, looking back up to 30 days: %s "
             "alone on all %d days, so without its atrazine the raw water keeps only the lake's spring residue and "
             "each day counts for %s and no other sub-watershed (plan 5.1). Apportioning each day by the "
             "tributaries' share of the atrazine past the stations, as if the lake were one mixed volume, puts the "
             "Tessel River first; the buoy shows a layered lake on every one of those days, so that reading is "
             "rejected." % (F["call"], F["days_total"], F["call"]))
    fm = [m for m in SEASON_M if bsm[F["call"]][m]]
    L.append("4. Counted each day above the trigger in its month: %s %s, none in %s; every other sub-watershed none "
             "in any month." % (F["call"], ", ".join("%s %d" % (m, bsm[F["call"]][m]) for m in fm),
                                 (lambda z: ", ".join(z[:-1]) + " or " + z[-1])([m for m in SEASON_M if m not in fm])))
    L.append("5. For the carbon, applied each dose setpoint in scada_pac_dose_setpoint_2026.csv (UTC) to the plant "
             "day's raw water pumped in daily_operating_report_2026.xlsx (06:00 to 06:00 next day) at 8.34 lb per "
             "million gallons per mg/L (SOP-WQ-07 3.2), minute by minute, over the minutes the feeder in "
             "scada_alarm_event_history_2026.csv was running with carbon: stopped from a MOTOR OVERLOAD TRIP until "
             "its next RUN STATUS ON, and feeding nothing from a HOPPER LEVEL LOW-LOW NO FEED alarm to its return: "
             "by local calendar month, %s lb in May, %s in June, %s in July and %s in August." % (fmt(pac["May"]), fmt(pac["June"]),
                                                                       fmt(pac["July"]), fmt(pac["August"])))
    L.append("6. Replayed SOP-WQ-07 3.2 and 3.3 day by day on the season's results (start the feed, or change its "
             "dose by Table 1, on a day above 3.0 ug/L; stop after two days in a row at or below 2.5 ug/L): the replay "
             "gives the plant's own eleven setpoint changes, 29 May to 6 August. Replayed again on the results "
             "without each sub-watershed's atrazine: without %s's, every day from 29 May to 6 August falls to the "
             "spring residue, so the feed never starts and every pound fed goes (%s); without any other "
             "sub-watershed's, no result moves, the replay is the plant's record and no pound goes. Booking each "
             "day's carbon to the sub-watershed behind that day would leave out the carbon fed after the last day "
             "above the trigger while the feed waited on its stop rule, all of August's %s lb among it."
             % (F["call"], ", ".join("%s %s lb" % (m, fmt(spared[F["call"]][m])) for m in PAC_M), fmt(pac["August"])))
    L.append("7. %s gets the program: %d days of %d, every other sub-watershed none.\n"
             % (F["call"], F["call_days"], F["days_total"]))
    L.append("## 4. Deliverable Answers\n")
    L.append("### cost_share_placement_2027.docx\n")
    L.append("1. The 2027 cost-share program goes to the %s sub-watershed." % F["call"])
    L.append("2. Days above the trigger each sub-watershed's atrazine caused, for the season (15 April to 31 October) "
             "and by month, April to October:")
    for k in [F["call"]] + others:
        L.append("   - %s: season %d; %s" % (k, per[k], ", ".join("%s %d" % (m, bsm[k][m]) for m in SEASON_M)))
    L.append("")
    L.append("### atrazine_sources_2026.xlsx\n")
    L.append("1. Powdered activated carbon fed in 2026 that the plant would not have fed without each sub-watershed's "
             "atrazine, pounds:")
    for k in [F["call"]] + others:
        L.append("   - %s: %s" % (k, ", ".join("%s %s" % (m, fmt(spared[k][m])) for m in PAC_M)))
    L.append("")
    L.append("### raw_water_atrazine_2026.png\n")
    L.append("1. The daily raw-water result from 15 April to 31 October 2026 against the 3.0 ug/L trigger line, the %d "
             "days above it marked." % F["days_total"])
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
