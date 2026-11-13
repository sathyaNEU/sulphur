"""task22 architecture 2: submission.md, the four answer blocks, every figure read from figures.json."""
import params as P


def _f(x, d=0):
    return ("{:,.%df}" % d).format(x)


def _join(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(figs, E, path):
    x = figs["_extra"]
    lt, ut = x["leak_table"], x["ur_table"]
    g, c = lt["golden"], lt["careful"]
    des = figs["R6_designated"]
    cho = figs["R7_changeout"]
    r1, r2, r3, r4, r5 = (figs[k] for k in ("R1_gas_in", "R2_billed_months", "R3_under", "R4_diversion",
                                             "R5_leak_pct"))
    sc = x["shortcut_sets"]
    sch = x["shortcut_changeouts"]
    air = sc["the logger study's straight line on the airport's air"]
    even = sc["each read spread evenly over its days"]
    nodiv = sc["no diversion subtracted"]
    alldiv = sc["every collapse in use booked as diversion"]
    careful = x["careful_designated"]
    plan = x["plan"]
    tp = x["tpar"]
    total_in = r1["fourteen districts, twelve months to September 2026"]
    airl = lt["the logger study's straight line on the airport's air"]
    outd = ["Riverside", "Lakeview", "Sundquist", "Halvorsen", "North End", "Elm Grove"]
    gaps = [g[d] - airl[d] for d in outd]
    gap_words = "%.1f to %.1f points" % (int(min(gaps) * 10) / 10.0, -int(-max(gaps) * 10) / 10.0)
    lines = []
    A = lines.append
    A("## Tags")
    A("")
    A("**Domain:** Energy Systems & Utilities, gas distribution (lost and unaccounted-for gas and the district gas "
      "balance).")
    A("**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).")
    A("")
    A("## Final Recommendation")
    A("")
    A("**Put %s into the 2027-2029 main replacement program, and send the 2027 meter changeout to %s.** Their leak "
      "loss in the twelve months to September 2026 was %s per cent of their gas in (Riverside %s, Lakeview %s, "
      "Sundquist %s). Reject the two-district list (%s) that the 2024-25 logger study's straight line on the airport's "
      "air gives: in the deep-snow winter of 2025-26 the gas in the buried services stayed near the soil's temperature, "
      "so that line books %s of each outdoor district's gas as meter error that was in fact leaking. Reject "
      "also the lists that spread each read evenly over its days (it adds Halvorsen) and that book every collapse in "
      "use as diversion (it drops Lakeview, whose new snowbirds took nothing)."
      % (_join(des), _join(cho), "%.2f to %.2f" % (min(g[d] for d in des), max(g[d] for d in des)),
         _f(r5["Riverside"], 2), _f(r5["Lakeview"], 2), _f(r5["Sundquist"], 2), _join(air), gap_words))
    A("")
    A("## Supplementary Questions")
    A("")
    A("### bpu_district_gas_balance_2023-10_2026-09.xlsx")
    A("")
    A("1. Monthly balance sheet: 504 rows, one per district and month from October 2023 to September 2026, Mcf at "
      "base conditions, with gas in at the regulator stations, the billed volume of the cycle-read meters carried "
      "to the calendar month, the under-registration of the meters without temperature compensation, the corrector "
      "customers, own use, third-party damage, gas taken without authorization and the leak loss left. Gas in: "
      "Riverside %s Mcf in January 2026 and Lakeview %s in December 2025 (each within 1.5 per cent), the fourteen "
      "districts %s Mcf in the twelve months to September 2026 (within 0.3 per cent). Billed volume carried to the "
      "month: College Hill %s Mcf in January 2026, North End %s in March 2026, Old Town %s in October 2025 and "
      "Halvorsen %s in October 2025 (each within 2 per cent)."
      % (_f(r1["Riverside, January 2026"], 1), _f(r1["Lakeview, December 2025"], 1), _f(total_in),
         _f(r2["College Hill, January 2026"], 1), _f(r2["North End, March 2026"], 1),
         _f(r2["Old Town, October 2025"], 1), _f(r2["Halvorsen, October 2025"], 1)))
    A("2. Twelve months to September 2026 sheet, by district: the meters without temperature compensation "
      "under-registered %s Mcf in Riverside and %s in Lakeview (each within 6 per cent), and %s per cent of their "
      "billed volume in College Hill, %s in Airport and %s in Halvorsen (each within 0.20 points); leak loss as a "
      "share of gas in: %s (each within 0.10 points)."
      % (_f(r3["Riverside, Mcf"]), _f(r3["Lakeview, Mcf"]), _f(r3["College Hill, per cent"], 2),
         _f(r3["Airport, per cent"], 2), _f(r3["Halvorsen, per cent"], 2),
         "; ".join("%s %s" % (k, _f(v, 2)) for k, v in r5.items())))
    A("3. Without authorization sheet: %d accounts took gas without authorization in the twelve months (within 1), "
      "%s Mcf of it in Elm Grove, %s in East Industrial and %s in Sundquist (each within 25 per cent); the new "
      "snowbirds whose winter use fell are not among them."
      % (r4["accounts"], _f(r4["Elm Grove, Mcf"]), _f(r4["East Industrial, Mcf"]), _f(r4["Sundquist, Mcf"])))
    A("4. The 2027 meter changeout (Rule 2) goes to %s; the main replacement program (Rule 1) takes %s."
      % (_join(cho), _join(des)))
    A("5. 2027 changeouts sheet: of the %d changeouts the 2027 plan schedules in Old Town and Downtown, %d will be "
      "done before November 1, 2027 (within 4 per cent)." % (plan["n"], figs["R8_done_before_season"]))
    A("")
    A("### lauf_program_2027_commission.pptx")
    A("")
    A("6. A short deck for the Commission: the districts entering the main replacement program and the changeout "
      "districts on its first slide, a bar chart of the fourteen districts' leak loss with the five above the 1.0 "
      "per cent line in blue, the reported loss's parts, and a bar chart of the under-registration by district with "
      "the seven changeout districts in blue.")
    A("")
    A("## Critical Components")
    A("")
    A("1. The meters without temperature compensation under-registered %s Mcf in Riverside and %s in Lakeview in the "
      "twelve months to September 2026 (%s per cent of their billed volume in Halvorsen, %s in College Hill), with "
      "the gas at the soil's temperature under the snow; the logger study's straight line on the air gives %s and "
      "%s per cent."
      % (_f(r3["Riverside, Mcf"]), _f(r3["Lakeview, Mcf"]), _f(r3["Halvorsen, per cent"], 2),
         _f(r3["College Hill, per cent"], 2), _f(ut["the logger study's straight line on the airport's air"]["Halvorsen"], 2),
         _f(ut["the logger study's straight line on the airport's air"]["College Hill"], 2)))
    A("2. Leak loss in the twelve months to September 2026: Riverside **%s**, Lakeview **%s**, Sundquist **%s** per "
      "cent of gas in, above the 1.0 per cent line; Halvorsen **%s** and Elm Grove **%s**, below it."
      % (_f(r5["Riverside"], 2), _f(r5["Lakeview"], 2), _f(r5["Sundquist"], 2), _f(r5["Halvorsen"], 2),
         _f(r5["Elm Grove"], 2)))
    A("3. Gas taken without authorization: **%d** accounts, %s Mcf in East Industrial and %s in Elm Grove; Lakeview's "
      "new snowbirds, whose winter use kept a reduced heating response and whose summers were whole, took none."
      % (r4["accounts"], _f(r4["East Industrial, Mcf"]), _f(r4["Elm Grove, Mcf"])))
    A("4. Billed volume carried to the month on each district's own regulator-station sendout: College Hill **%s** Mcf "
      "in January 2026 (the student rentals empty over the break) and North End **%s** in March 2026."
      % (_f(r2["College Hill, January 2026"], 1), _f(r2["North End, March 2026"], 1)))
    A("")
    A("## Step-by-Step")
    A("")
    A("1. Rebuilt each regulator station's faulty gas days from the city gate less the other stations and the gate's "
      "own small difference: Riverside's January 12 to 25 communication gap, Lakeview's December transducer failure "
      "(the corrector substituted 25 psig for 35) and Westgate's stuck temperature transmitter; Riverside's January "
      "gas in is %s Mcf and the fourteen districts' twelve months %s." % (_f(r1["Riverside, January 2026"], 1),
                                                                         _f(total_in)))
    A("2. Turned the AMR reads into actual-to-actual periods per meter (the June 2025 extract's repeated rows dropped, "
      "estimated reads folded into the next actual read, four-dial rollovers and multipliers, final and initial reads "
      "at each exchange) and spread each period's billed volume over its days in proportion to its district's daily "
      "regulator-station volume: College Hill's January 2026 is %s Mcf, where spreading evenly over the days gives "
      "%s, because the student rentals sat nearly empty from mid-December to mid-January."
      % (_f(r2["College Hill, January 2026"], 1), _f(figs["_extra"].get("careful_r2_ch", 0.0), 1)))
    A("3. Corrected the meters without temperature compensation (the register's flag, or the model code where it is "
      "blank) to base conditions with the gas temperature the meter saw: outdoors the soil at 20 inches plus %.3f of "
      "the air's difference from it and %.1f F of the house wall's warmth when the air is below 45 F, fitted on the "
      "2024-25 loggers and matched by the commercial correctors' own gas temperatures through 2025-26; indoors, near "
      "basement temperature. The logger study's straight line on the airport's air fitted its own winter, when air "
      "and soil fell together, but in 2025-26 the snow held the soil near freezing while the air fell as far, so the "
      "line puts Halvorsen's under-registration at %s per cent against %s." % (
          tp.get("k", 0), tp.get("wall", 0), _f(ut["the logger study's straight line on the airport's air"]["Halvorsen"], 2),
          _f(r3["Halvorsen, per cent"], 2)))
    A("4. Took each account's monthly use against its own weather response in the year before: %d collapsed for three "
      "months or more reaching into the heating season, outside a vacancy or an exchange (a student rental's summer "
      "away recurs every year); those whose summer base load also went (bypasses) or whose "
      "winter use lost its heating response but kept its base (furnace taps) took gas without authorization (%d "
      "accounts), and those whose winter use kept a reduced heating response and whose summer returned were away "
      "(Lakeview's new snowbirds). Booking every collapse as diversion counts %d accounts and drops Lakeview's leak "
      "loss to %s per cent." % (x["careful_diversion_accounts"], r4["accounts"], x["careful_diversion_accounts"],
                                _f(lt["every collapse in use booked as diversion"]["Lakeview"], 2)))
    A("5. Leak loss is gas in less the billed volume, the under-registration, the corrector customers, own use, the "
      "damage reports and the gas taken without authorization: %s. The careful but hurried route (the air line, "
      "reads spread evenly, every collapse booked) leaves only %s over the line." % (
          "; ".join("%s %s" % (P.DNAME[k] if k in P.DNAME else k, _f(v, 2)) for k, v in g.items()),
          _join(careful)))
    A("6. Rule 2 on the under-registration: %s exceed 3.5 per cent of the volume billed for their meters without "
      "compensation; College Hill, Airport and East Industrial, where many of those meters are inside, do not "
      "(the air line puts them over: %s). Westgate and Heritage Park have fewer than 100 such meters." % (
          _join(cho), _join(sorted(set(sch["the logger study's straight line on the airport's air"]) - set(cho)))))
    A("7. The 2027 plan schedules %d changeouts in Old Town and Downtown from April 5 to October 29, 2027. In 2024 and "
      "2025 crews finished outside meters within days of their planned date and inside meters (which need the "
      "customer home) weeks later or not at all; at those paces %d are done before November 1, 2027, not %d."
      % (plan["n"], figs["R8_done_before_season"], plan["n"]))
    A("")
    A("No other set survives. The same five districts come out with each read spread on a base-and-degree-day fit of "
      "the district's sendout, with the gas temperature tied to the commercial correctors' instead of the soil, and "
      "under the air coefficient 20 per cent either way, the indoor temperature 2 F either way, and the damage, own "
      "use and diversion volumes 20 per cent either way. Each shortcut lands on a different list: the air line on %s; "
      "the 2019 consultant's monthly air on none; reads spread evenly on %s; no diversion on %s; every collapse as "
      "diversion on %s." % (_join(air), _join(even), _join(nodiv), _join(alldiv)))
    open(path, "w").write("\n".join(lines) + "\n")
