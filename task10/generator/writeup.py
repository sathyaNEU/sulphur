"""task10 architecture 5: submission.md, the four platform blocks, drafted from figures.json only."""
import json
import os


def r1(v):
    return "%.1f" % v


def r0(v):
    return "%d" % int(round(v))


def blocks(F):
    z = {k: F["zones"][k] for k in ("Ashcombe Road", "Charlecote Way", "Fenwick Street", "Hartwell Common")}
    A, C, Fz, H = z["Ashcombe Road"], z["Charlecote Way"], z["Fenwick Street"], z["Hartwell Common"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Energy Systems & Utilities (load, price & renewable forecasting: distribution network design-day "
               "peak demand).  \n**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## Final Recommendation\n")
    out.append("**Commit reinforcement at Ashcombe Road and Hartwell Common for winter 2027/28; Charlecote Way and Fenwick "
               "Street hold firm capacity with the flexibility contracted for that winter.** Credited at what Corvane Flex "
               "delivers on the design day, %s per megawatt scheduled, the 2027/28 flexibility leaves Ashcombe Road at "
               "%s MW against %s MW firm and Hartwell Common at %s MW against %s MW; the %s per megawatt their event "
               "records show counts the demand that rose at %s and %s, across their 11 kV open points, in the same "
               "half-hours, and on that figure no primary would be reinforced.\n"
               % (r1(A["delivery"]), r0(A["after"]), r1(A["firm"]), r0(H["after"]), r1(H["firm"]), r1(A["measured"]),
                  A["linked"], H["linked"]))
    out.append("## Supplementary Questions\n")
    out.append("### halverton_primary_capacity_2027-28.xlsx\n")
    zs = (("Ashcombe Road", A), ("Charlecote Way", C), ("Fenwick Street", Fz), ("Hartwell Common", H))
    S2 = F["sens"]["6.0"]

    def names(ps):
        return "all four" if len(ps) == 4 else ", ".join(ps[:-1]) + " and " + ps[-1]
    out.append("1. A Zones sheet with one row per flexibility zone, in the order Ashcombe Road CMZ, Charlecote Way CMZ, "
               "Fenwick Street CMZ, Hartwell Common CMZ, giving the zone, its primary and asset code, the provider and "
               "the megawatts contracted for 2027/28, then the provider's delivery per megawatt scheduled on the design "
               "day: %s at Ashcombe Road, %s at Charlecote Way, %s at Fenwick Street and %s at Hartwell Common (Corvane "
               "Flex %s at both its zones, Quillon Energy Services %s at both of its)."
               % (r1(A["delivery"]), r1(C["delivery"]), r1(Fz["delivery"]), r1(H["delivery"]), r1(A["delivery"]),
                  r1(C["delivery"])))
    out.append("2. The megawatts credited to each primary on its 2027/28 contract: %s MW at Ashcombe Road, %s at "
               "Charlecote Way, %s at Fenwick Street and %s at Hartwell Common."
               % (r0(A["credited"]), r0(C["credited"]), r0(Fz["credited"]), r0(H["credited"])))
    out.append("3. Each primary's design-day demand after the credited flexibility against its firm capacity: %s, so "
               "%s exceed firm capacity and %s do not."
               % ("; ".join("%s %s MW against %s MW" % (nm, r0(Z["after"]), r1(Z["firm"])) for nm, Z in zs),
                  " and ".join(nm for nm, Z in zs if Z["over"]), " and ".join(nm for nm, Z in zs if not Z["over"])))
    out.append("4. A clustered column chart below the table: for each zone primary, its design-day demand before and "
               "after the credited flexibility beside its firm capacity, in MW, the after-flexibility column standing "
               "above firm capacity at %s and below it at %s."
               % (" and ".join(nm for nm, Z in zs if Z["over"]), " and ".join(nm for nm, Z in zs if not Z["over"])))
    out.append("5. How far each primary to reinforce exceeds firm capacity on the design day: %s."
               % " and ".join("%s by %s MW" % (nm, r0(Z["over_by"])) for nm, Z in zs if Z["over"]))
    out.append("6. The primaries whose demand after their flexibility would exceed firm capacity on a working weekday "
               "of winter 2027/28 at a daily mean of minus %s C: %s."
               % (r1(S2["degrees_below_zero"]), names(S2["commit"])))
    out.append("\n### capex_review_2027-28.pptx\n")
    out.append("7. Slides for the capital expenditure review that name Ashcombe Road and Hartwell Common as the primaries "
               "to reinforce for winter 2027/28, state that Charlecote Way and Fenwick Street hold firm capacity on the "
               "design day with their contracted flexibility, and carry the same chart of demand against firm capacity.\n")
    out.append("## Critical Components\n")
    out.append("1. On the flexibility events at Ashcombe Road, Fenwick Street and Hartwell Common, the primary across an "
               "11 kV open point from each (%s, %s, %s) rose in the half-hours ending 17:30 and 18:00 by **%s**, **%s** "
               "and **%s MW** on average as the zone primary fell, which is not a reduction its provider delivers "
               "(section 6 of the guideline), so it is netted from the zone's fall; no neighbour of Charlecote Way rose."
               % (A["linked"], Fz["linked"], H["linked"], r1(A["linked_rise"]), r1(Fz["linked_rise"]),
                  r1(H["linked_rise"])))
    out.append("2. Net of those rises the providers' own reduction falls as the day gets colder; at the design day's minus "
               "3.0 C Corvane Flex delivers **%s** and Quillon Energy Services **%s** per MW scheduled, not the **%s** per "
               "MW the event records show at Ashcombe Road, Fenwick Street and Hartwell Common."
               % (r1(A["delivery"]), r1(C["delivery"]), r1(A["measured"])))
    out.append("3. On the 2027/28 contracts the flexibility credits **%s**, **%s**, **%s** and **%s MW**, leaving "
               "Ashcombe Road at **%s MW** against %s MW firm and Hartwell Common at **%s MW** against %s MW."
               % (r0(A["credited"]), r0(C["credited"]), r0(Fz["credited"]), r0(H["credited"]), r0(A["after"]),
                  r1(A["firm"]), r0(H["after"]), r1(H["firm"])))
    out.append("4. Charlecote Way (**%s MW**, firm %s MW) and Fenwick Street (**%s MW**, firm %s MW) stay within firm "
               "capacity after their credited flexibility.\n" % (r0(C["after"]), r1(C["firm"]), r0(Fz["after"]),
                                                                   r1(Fz["firm"])))
    out.append("## Step-by-Step\n")
    T = F["event_temperature_c"]
    out.append("1. Mapped both SCADA point names in primary_demand_halfhourly_2023-2026.csv to asset codes through "
               "primary_substation_register.xlsx, kept each quality G half-hour once and read its end in UK local time.")
    out.append("2. Kept the latest revision of each instruction in flexibility_events_2024-2026.csv, a cancelled one at "
               "0.0 MW, and each hour of halverton_weather_hourly_2023-2026.csv at its checked reading, averaged over "
               "the GMT day.")
    out.append("3. Corrected each zone primary's 2025/26 daily peaks on working weekdays outside 24 December to 2 "
               "January and outside its scheduled days to the design condition (a level and one slope below 15.5 C) "
               "and grew the result by the DFES rates and the qualifying connections in "
               "load_growth_register_2026-27.xlsx (guideline sections 3 and 4).")
    out.append("4. Measured each event's fall at the zone primary in the half-hours ending 17:30 and 18:00 against a "
               "weather-adjusted baseline fitted on its other working weekdays: %s per MW scheduled at Ashcombe Road, "
               "%s at Fenwick Street, %s at Hartwell Common and %s at Charlecote Way; carried to the 2027/28 contracts, "
               "that keeps all four primaries within firm capacity and commits none (the shallow route)."
               % (r1(A["measured"]), r1(Fz["measured"]), r1(H["measured"]), r1(C["measured"])))
    out.append("5. Read the same half-hours at every primary each zone's open points reach in network_feeders_11kv.xlsx, "
               "on a baseline fitted without the zone's event days: %s rose %s MW on Ashcombe Road's events, "
               "%s %s MW on Fenwick Street's and %s %s MW on Hartwell Common's, while no neighbour of "
               "Charlecote Way rose, so each of those zones' fall includes demand that rose across the open point, which "
               "section 6 of the guideline does not credit to the provider."
               % (A["linked"], r1(A["linked_rise"]), Fz["linked"], r1(Fz["linked_rise"]), H["linked"],
                  r1(H["linked_rise"])))
    out.append("6. Netted each linked primary's rise from the zone's fall event by event and regressed the provider's "
               "reduction per MW scheduled on the event day's daily mean temperature: %s per MW for Corvane Flex at "
               "Ashcombe Road, %s at Hartwell Common, %s for Quillon Energy Services at Charlecote Way and %s at Fenwick "
               "Street at minus 3.0 C, inside the event days' own range of minus %s to %s C (%s, %s, %s and %s on the "
               "average event day)."
               % (r1(A["delivery"]), r1(H["delivery"]), r1(C["delivery"]), r1(Fz["delivery"]), r1(T["coldest_below_zero"]),
                  r1(T["mildest"]), r1(A["avg_delivery"]), r1(H["avg_delivery"]), r1(C["avg_delivery"]),
                  r1(Fz["avg_delivery"])))
    out.append("7. Credited those on the megawatts in flexibility_contract_awards_2027-28.pdf and compared with Appendix A "
               "of capacity_assessment_guideline_2026.pdf: Ashcombe Road at %s MW against %s exceeds firm capacity by "
               "%s MW and Hartwell Common at %s MW against %s by %s MW; Charlecote Way at %s against %s and Fenwick "
               "Street at %s against %s hold."
               % (r0(A["after"]), r1(A["firm"]), r0(A["over_by"]), r0(H["after"]), r1(H["firm"]), r0(H["over_by"]),
                  r0(C["after"]), r1(C["firm"]), r0(Fz["after"]), r1(Fz["firm"])))
    out.append("8. Checked the correction's straight-line form on winter 2023/24, which ran no flexibility: fitted on its "
               "working weekdays as mild as the 2025/26 days the correction uses, it meets that winter's sub-zero working "
               "weekdays within %s MW on average at every zone primary, closer than a quadratic at each."
               % r1(F["validation"]["linear_bias_max"]))
    held = [p for p in S2["commit"] if p not in S2["held_credit_commit"]]
    out.append("9. Read the same correction and the same provider regressions at a daily mean of minus %s C: each provider "
               "delivers less per MW scheduled on the colder day while the demand rises, so %s exceed firm capacity; "
               "carrying the design day's credit to that day instead leaves %s within it, and the zone's own fall leaves "
               "Fenwick Street within it.\n"
               % (r1(S2["degrees_below_zero"]), names(S2["commit"]), " and ".join(held)))
    fall = [p for p in F["fall_at_day_call"]]
    out.append("No other conclusion survives the files. The zone primary's own fall, against a weather-adjusted baseline "
               "or the ten previous weekdays, counts the demand that rose at the neighbour, and the ten-day baseline also "
               "sits below the cold event days it is set against, so it files all four primaries. Read at minus 3.0 C, "
               "the same fall credits %s, %s, %s and %s per MW and files %s alone (%s MW over firm), because it counts as "
               "the providers' reduction the demand that rose across the open points, which is not a reduction its provider "
               "delivers: section 6 of the guideline credits only that, and the award notice measures what a provider "
               "delivers on its own metered assets. Taking the linked primary as the control adds that rise twice (%s per "
               "MW at Ashcombe Road) and files none. The zone and its linked primary taken together give the netting's "
               "provider reduction exactly (%s per MW at minus 3.0 C at Ashcombe Road). Crediting the providers at the "
               "average event day rather than at the design day keeps the same two primaries over firm capacity but "
               "credits %s, %s, %s and %s MW, which is not the reduction section 6 of the guideline credits, and at minus "
               "%s C it leaves Charlecote Way and Fenwick Street within firm capacity; on the design day's credit, "
               "Ashcombe Road and Hartwell Common need reinforcement."
               % (r1(A["fall_delivery"]), r1(C["fall_delivery"]), r1(Fz["fall_delivery"]), r1(H["fall_delivery"]),
                  " and ".join(fall), r1(A["fall_over_by"]), r1(A["did"]), r1(A["pair"]), r0(A["avg_credited"]),
                  r0(C["avg_credited"]), r0(Fz["avg_credited"]), r0(H["avg_credited"]), r1(S2["degrees_below_zero"])))
    return "\n".join(out) + "\n"


def write(F, path):
    open(path, "w", encoding="utf-8").write(blocks(F))
