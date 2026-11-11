"""figures.json and submission.md, both from golden.compute's figures: every number the four blocks state is a key
the generator wrote, at the rounding the blocks state it."""
import json

import analysis as A
import golden as GD
import params as P

W = list(P.PEAK_WEEKS)


def fmt(n):
    return "{:,}".format(int(n))


def wk(ws_):
    return GD.weeks_text(ws_)


def zones_phrase(ev):
    """'week 48 in both zones', 'P1 week 48 and P2 weeks 48 to 50', 'no week in either zone'."""
    p1, p2 = ev["P1"], ev["P2"]
    if not p1 and not p2:
        return "in no week in either zone"
    if p1 == p2:
        return "in %s %s in both zones" % ("week" if len(p1) == 1 else "weeks", wk(p1))

    def one(z, w):
        if not w:
            return "%s in no week" % z
        return "%s %s %s" % (z, "week" if len(w) == 1 else "weeks", wk(w))
    return "in " + ", ".join(one(z, w) for z, w in (("P1", p1), ("P2", p2)))


def flat(figs, G, f, rivals):
    tab = G["cal"]["table"]
    over = {"%d %s" % (r.year, r.group): round(100 * r.over, 1) for r in tab.itertuples(index=False)}
    out = dict(figs)
    out["over_by_year"] = over
    out["rivals"] = rivals
    out["limits"] = dict(P.LIMIT)
    out["aisles"] = dict(P.AISLES)
    out["aisles_old"] = dict(P.AISLES_OLD)
    out["peak_weeks"] = W
    out["d_2025_peak"] = rivals["d_2025_peak"]
    out["lines_k_2027_wk47"] = rivals["lines_k_47"]
    out["budget_k_2027_wk47"] = rivals["budget_k_47"]
    out["bands"] = dict(rivals["bands"], range_pct=8, r1_pct=1)
    out["conventions"] = {"range_coverage_pct": 80, "iso_weeks_2026": 53, "cost_centres": [4111, 4112, 4113, 4150],
                          "shift_days_2025_2027": 728, "black_friday": {"2025": "28 November", "2027": "26 November"},
                          "bf_days": [26, 28], "years": [2022, 2023, 2024, 2025, 2026, 2027], "week_after_peak": 51,
                          "density_reported": 1.8, "aisles_before": [8, 7], "aisles_after": [12, 11]}
    return out


def write_figures(path, figs):
    json.dump(figs, open(path, "w"), indent=1, sort_keys=True, default=str)


def submission(figs):
    h = figs["hours"]
    rg = figs["range"]
    ag = figs["agency"]
    hu = figs["hurried"]
    rt = figs["routes"]
    lines = []
    lines.append("# task4: Saarnela's 2027 peak, the evening shifts and the agency booking\n")
    lines.append("## Tags\n")
    lines.append("**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (a "
                 "third-party fulfilment centre's peak labour plan: forecasting each pick zone's picker hours once a "
                 "second brand shares its zones).\n")
    lines.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    lines.append("## Final Recommendation\n")
    lines.append(
        "Agree the evening shift in weeks %s in both small-parts zones, P1 and P2, and book %s agency picker hours "
        "over the 2027 peak (%s in weeks 46 to 50); week 46 runs on day shifts alone. Not the draft plan's route (the "
        "client's budget as issued over its pooled overstatement, the 2025 peak's hours a line and the pilot's time a "
        "line), which opens the evening shift %s only and books %s hours: it plans 2027's day shifts at "
        "2025's crowding though the limit puts %d and %d pickers on the floor, Huippu Sport at its polybag pilot, "
        "Kotikaari at an overstatement its modest 2027 plan does not carry, and Black Friday a week late.\n" % (
            wk(figs["evening"]["P1"]), fmt(figs["agency_total"]), ", ".join(fmt(ag[w]) for w in W),
            zones_phrase(hu["evening"]), fmt(hu["agency_total"]), figs["limits"]["P1"], figs["limits"]["P2"]))
    lines.append("## Supplementary Questions\n")
    lines.append("### saarnela_peak_plan_2027.xlsx\n")
    lines.append(
        "The workbook has five sheets: Plan (one row per ISO week 46 to 50 and pick zone P1, P2, B1: the lines "
        "expected, the day-shift capacity at the zone's limit, the evening-shift verdict, the picker hours with their "
        "80 per cent range, the own pickers' hours and the agency hours, then the agency hours by week), Volumes (each "
        "brand's and group's weekly lines, the budget as issued beside the lines expected), Forecast record (each "
        "budget's overstatement against its plan's growth), Time a line (the task-time model and the congestion "
        "curve) and Routes (each shorter route's evening-shift weeks and agency hours).\n")
    lines.append(
        "1. Picker hours each pick zone will need, paid hours to the nearest 10 with the range put at 80 per cent "
        "(sheet Plan; each figure graded within %d per cent, each range end within 8 per cent): " % figs["rivals"]["hours_band_pct"]
        + "; ".join("week %d P1 %s (%s to %s), P2 %s (%s to %s), B1 %s (%s to %s)" % (
            w, fmt(h["P1"][w]), fmt(rg["P1"][w][0]), fmt(rg["P1"][w][1]), fmt(h["P2"][w]), fmt(rg["P2"][w][0]),
            fmt(rg["P2"][w][1]), fmt(h["B1"][w]), fmt(rg["B1"][w][0]), fmt(rg["B1"][w][1])) for w in W) + ".\n")
    lines.append(
        "2. Agency picker hours to book on top of the own pickers, to the nearest 10 (sheet Plan; each graded within "
        "%d per cent): %s; %s over the peak.\n" % (figs["rivals"]["agency_band_pct"],
                                                   "; ".join("week %d %s" % (w, fmt(ag[w])) for w in W),
                                                   fmt(figs["agency_total"])))
    lines.append(
        "3. Whether each small-parts zone needs the evening shift: P1 in weeks %s, P2 in weeks %s; neither in week "
        "46, where the day shifts pick the week's lines below the limit (P1 at %.2f and P2 at %.2f of the day "
        "shifts' capacity at the limit).\n" % (wk(figs["evening"]["P1"]), wk(figs["evening"]["P2"]),
                                                figs["ratio"]["P1"][46], figs["ratio"]["P2"][46]))
    lines.append(
        "4. The share by which Kotikaari's year-ahead forecasts of its peak weeks have overstated the order lines it "
        "placed in those weeks: %.1f per cent (graded within %.1f to %.1f), the October budgets' order lines over weeks "
        "46 to 50 of 2022 to 2025 against the order lines the WMS's order import records for those weeks, both "
        "groups.\n" % (figs["r2"], *figs["bands"]["r2"]))
    lines.append(
        "5. How much longer a Huippu Sport order line will take to pick than a Kotikaari one in the small-parts zones "
        "in the 2027 peak: %.2f minutes of task time (graded within %.2f to %.2f), %.2f against %.2f.\n" % (
            figs["r4"], *figs["bands"]["r4"], figs["t_hui"], figs["t_kot"]))
    lines.append("### saarnela_peak_plan_2027.docx\n")
    lines.append(
        "6. One page for the management team: the recommendation (the evening-shift weeks by zone and the agency "
        "hours by week), a table of each week's picker hours by zone with the ranges, the verdicts and the agency "
        "hours, one chart of each small-parts zone's weekly lines against its day-shift capacity at the limit, and "
        "the drivers the plan rests on beside the draft's result.\n")
    lines.append("## Critical Components\n")
    lines.append(
        "1. Aisle congestion, measured with the line mix held fixed: a line takes **%.2f minutes** longer at 1.8 "
        "pickers logged in an aisle than on an empty floor (graded within %.2f to %.2f), on the WMS zone hours' task "
        "minutes regressed on lines by handling class, extra units, zone and a convex term in pickers per aisle "
        "(the aisles as the standard gives them before and after January 2024). The 2025 peak's day shifts put "
        "%.2f pickers on the floor an aisle, against the two an aisle of 2027's day shifts at the limit, so its hours a "
        "line understate 2027's.\n" % (figs["r3"], *figs["bands"]["r3"], figs["d_2025_peak"]))
    lines.append(
        "2. The 2027 budget's expected overstatement: **%.1f per cent** for Kotikaari small parts (graded within %.1f "
        "to %.1f), against the pooled %.1f: the October budgets' overstatement over their whole year grows with the "
        "commercial plan's growth (%s), and the 2027 plan is %d per cent; Huippu Sport's %d per cent plan points to "
        "%.1f per cent.\n" % (figs["r5"]["K_sp"], *figs["bands"]["r5_K_sp"], figs["r2"], "; ".join("%s %.1f" % (k, v) for k, v in
                                                                             sorted(figs["over_by_year"].items())),
                               figs["plan_growth"]["K"][0], figs["plan_growth"]["H"][0], figs["r5"]["H_sp"]))
    lines.append(
        "3. Black Friday's week: **%.1f per cent** of the 2027 peak's Kotikaari small-parts lines fall in week 47 "
        "(graded within %.1f to %.1f), against the budget's %.1f: the budget phases 2027 by 2025's week numbers, "
        "2026 has 53 ISO weeks, and Black Friday moves from week 48 in 2025 to week 47 in 2027 (26 November).\n" % (
            figs["r6"], *figs["bands"]["r6"], figs["r6_budget"]))
    lines.append(
        "4. The 2025 peak's picker hours as the payroll records them: **%s** in P1, **%s** in P2 and **%s** in B1 "
        "(weeks 46 to 50, worked hours, graded within 1 per cent), with %.3f of each paid day-shift hour logged in "
        "to a zone.\n" % (fmt(figs["r1"]["P1"]), fmt(figs["r1"]["P2"]), fmt(figs["r1"]["B1"]), figs["logged_share"]))
    lines.append("## Step-by-Step\n")
    steps = [
        "Conform the records: the old payroll export (semicolon, decimal commas, cost centres 4111 to 4150) onto the "
        "new one, its March 2024 correction run dropped, packing hours left out; the WMS zone hours exported twice on "
        "three dates de-duplicated; pickers logged per aisle with the standard's aisles (8 and 7 before 8 January "
        "2024, 12 and 11 after); the 2025 peak's picker hours come to %s, %s and %s (component 4)." % (
            fmt(figs["r1"]["P1"]), fmt(figs["r1"]["P2"]), fmt(figs["r1"]["B1"])),
        "The forecast record (ask 4): the October budget rounds of the archive, the latest issue of each week, "
        "against the order lines Kotikaari placed in the same weeks (the order import): %.1f per cent over the peak "
        "weeks of 2022 to 2025. The lines picked in those weeks run lower (the dense peaks' backlog spills into week "
        "51), and the latest rolling forecasts land within a few per cent and say nothing about the year-ahead lead."
        % figs["r2"],
        "The budget's overstatement against its plan (component 2): over each year both groups' overstatement rises "
        "with the plan's growth (a log-log fit through the eight budget-years); the 2027 plan of %d per cent for "
        "Kotikaari small parts gives %.1f per cent, not the pooled %.1f, which would take out lines the modest plan "
        "never added." % (figs["plan_growth"]["K"][0], figs["r5"]["K_sp"], figs["r2"]),
        "The weekly profile (component 3): 2025's orders by day, moved 728 days onto the same weekday of 2027 (Black "
        "Friday 28 November 2025 onto 26 November 2027), released by the standard's rule on 2027's working days and "
        "scaled to the budget's growth over 2025 less the expected overstatement: week 47 carries %.1f per cent of "
        "Kotikaari's small-parts peak, not the budget's %.1f; Huippu Sport's own daily orders re-keyed the same way."
        % (figs["r6"], figs["r6_budget"]),
        "The time a line (component 1, ask 5): the zone-hour regression gives each handling class's minutes, %.3f a "
        "unit after the first and %.3f for a Huippu Sport line, with congestion %.2f minutes at 1.8 pickers an aisle; "
        "a fit without the density term returns impossible class rates, and a straight-line density term fits four "
        "times worse. Huippu Sport's peak mix comes from its article lines of November and December 2025 with the "
        "item master's classes and the slotting's zones: %.2f minutes a line against Kotikaari's %.2f, +%.2f; the "
        "pilot's own lines (%.2f against P2's %.2f, all polybag apparel) give %.2f." % (
            figs["fit"]["coef"]["unit"], figs["fit"]["coef"]["HUI"], figs["r3"], figs["t_hui"], figs["t_kot"],
            figs["r4"], hu["pilot_t"], hu["p2_t"], hu["r4"]),
        "The plan (asks 1 to 3): each zone-week's lines against what the day shifts at the limit can pick at the "
        "week's time a line with the congestion each hour's pickers give (the logged share by hour from the 2024 and "
        "2025 peak days); P1 and P2 exceed it in weeks %s by %.2f to %.2f times and week 46 stays at %.2f and %.2f, "
        "so the evening shift opens in weeks %s and the day shifts run at %d and %d pickers." % (
            wk(figs["evening"]["P1"]), min(figs["ratio"][z][w] for z in A.Z_SMALL for w in figs["evening"][z]),
            max(figs["ratio"][z][w] for z in A.Z_SMALL for w in figs["evening"][z]), figs["ratio"]["P1"][46],
            figs["ratio"]["P2"][46], wk(figs["evening"]["P1"]), figs["limits"]["P1"], figs["limits"]["P2"]),
        "The ranges and the agency (asks 1 and 2): the range carries the budget's residual error at the year-ahead "
        "lead (%.3f on the log scale), the re-keyed profile's weekly error (%.3f, 2024 onto 2025) and the model's "
        "(%.3f), through the floor's own congestion; the agency books every hour above the own pickers' planned "
        "hours less the 2025 peak's sickness absence: %s hours." % (figs["sd"]["level"], figs["sd"]["week"],
                                                                  figs["sd"]["model"], fmt(figs["agency_total"])),
        "The draft's route, the budget as issued over the pooled %.1f per cent with the 2025 hours a line and the "
        "pilot's time a line, opens the evening shift %s only and books %s hours; put right alone, the calendar opens "
        "it %s (%s hours), the calibration %s (%s), the congestion %s (%s) and Huippu Sport's mix %s (%s)." % (
            hu["r2_applied"], zones_phrase(hu["evening"]), fmt(hu["agency_total"]),
            zones_phrase(rt["calendar"]["evening"]), fmt(rt["calendar"]["agency_total"]),
            zones_phrase(rt["calibration"]["evening"]), fmt(rt["calibration"]["agency_total"]),
            zones_phrase(rt["congestion"]["evening"]), fmt(rt["congestion"]["agency_total"]),
            zones_phrase(rt["huippu"]["evening"]), fmt(rt["huippu"]["agency_total"])),
    ]
    for i, s in enumerate(steps, 1):
        lines.append("%d. %s\n" % (i, s))
    lines.append(
        "Why no other conclusion survives: the draft's route and every route that puts one judgment right land a "
        "different set of evening-shift weeks, because the four move the weeks in different directions: the 2025 "
        "rate holds only below the density 2027's day shifts run at, the pilot measured polybag apparel, the pooled "
        "overstatement belongs to budgets that planned more growth, and a week-numbered phasing after a 53-week year "
        "puts Black Friday in week 48. Aligning 2025's days to 2027's by date instead of weekday puts Black Friday on a "
        "Sunday and is ruled out by its own record (each year's spike falls on the Friday after the fourth Thursday "
        "of November); a straight-line or cubic congestion term fits the zone hours far worse; every defensible "
        "variant (a quadratic term, a flat logged share, the 2024 and 2025 profiles averaged, a linear calibration, "
        "one through the origin or on the peak weeks) keeps weeks 47 to 50, and so does each fitted input moved 20 "
        "per cent.\n")
    return "\n".join(lines)
