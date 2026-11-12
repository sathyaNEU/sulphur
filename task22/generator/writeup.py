"""task22 submission.md: the four answer blocks, drafted from figures.json so every figure they state is one the
generator computed."""
import analysis as A
import deliver as DL


def n0(x):
    return "{:,.0f}".format(x)


def n1(x):
    return "{:,.1f}".format(x)


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def swap(fo, gold, prefix):
    """Which feeder a shortcut route puts in, and for which, read off the route's own answer."""
    ans = next(r["answer"] for r in fo["routes"] if r["name"].startswith(prefix))
    ins, outs = [f for f in ans if f not in gold], [f for f in gold if f not in ans]
    return " and ".join("%s in for %s" % (a, b) for a, b in zip(ins, outs))


def write(figs, G, fo, path):
    T = figs
    s = T["R9_sweep"]
    ntl = T["ntl_all"]
    c = T["careful_ntl"]
    cs = T["careful_sweep"]
    np_ = T["R7_new_peaks"]
    apps = sorted(np_)
    lines = []
    a = lines.append
    a("## Tags")
    a("")
    a("**Domain:** Energy Systems & Utilities, grid operations (distribution losses and the feeder energy balance).")
    a("**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).")
    a("")
    a("## Final Recommendation")
    a("")
    a("**Sweep %s, %s, %s and %s in 2027:** they carried %s, %s, %s and %s MWh of non-technical loss in the twelve "
      "months to September 2026, and the next feeder, %s, carried %s. Reject the four that the residual gives on the "
      "old loss study's percentages, today's GIS and the storm gap carried at the feeder's average (%s, %s, %s and "
      "%s): APT-3's excess is its own network losses (%s MWh at its 2026 loads, not the study's %s), and NTH-3 looks "
      "high only while the lateral it passed to NTH-4 on April 21 is counted on NTH-4 for the whole year." % (
          s[0], s[1], s[2], s[3], n0(ntl[s[0]]), n0(ntl[s[1]]), n0(ntl[s[2]]), n0(ntl[s[3]]), T["fifth_feeder"],
          n0(T["fifth_ntl"]), cs[0], cs[1], cs[2], cs[3], n0(T["R4_technical"]["APT-3"]),
          n0(T["careful_tech_apt3_26"])))
    a("")
    a("## Supplementary Questions")
    a("")
    a("### %s" % DL.MEMO)
    a("")
    a("1. One page to the utility director: the four feeders to sweep in 2027 with their non-technical loss in the "
      "twelve months to September 2026 (%s %s, %s %s, %s %s and %s %s MWh, each within the band in answer 3), the next "
      "feeder (%s, %s MWh), why APT-3 and NTH-3 are not on the list, the line loss rise and its split, the 2027 "
      "technical losses, and a horizontal bar chart of all fourteen feeders' non-technical loss with the four in "
      "blue." % (s[0], n0(ntl[s[0]]), s[1], n0(ntl[s[1]]), s[2], n0(ntl[s[2]]), s[3], n0(ntl[s[3]]),
                 T["fifth_feeder"], n0(T["fifth_ntl"])))
    a("")
    a("### %s" % DL.WORKBOOK)
    a("")
    r1 = T["R1_energy_in"]
    r2 = T["R2_membership"]
    a("2. Monthly balance: 504 rows, one per feeder and month from October 2023 to September 2026, columns month, "
      "feeder, customers at month end, energy in at the breaker, received from customers' generation, delivered "
      "through customers' meters, large power meters, city street and area lights, technical losses and "
      "non-technical loss (MWh). NTH-4 served %d customers at the end of March 2026 and %d at the end of May 2026 "
      "(each within 3). CHL-3's energy in is %s MWh for January 2026 (within 3 per cent) and %s MWh for the twelve "
      "months to September 2026 (within 0.6 per cent); the fourteen feeders' is %s MWh (within 0.12 per cent)." % (
          r2["NTH-4 customers, 31 March 2026"], r2["NTH-4 customers, 31 May 2026"],
          n1(r1["CHL-3, January 2026"]), n1(r1["CHL-3, twelve months to September 2026"]),
          n1(r1["fourteen feeders, twelve months to September 2026"])))
    r3 = T["R3_lights"]
    r4 = T["R4_technical"]
    r5 = T["R5_ntl"]
    a("3. Twelve months to September 2026, by feeder: NTH-4's customers' meters recorded %s MWh and NTH-3's %s "
      "(each within 1.5 per cent); the city's lights used %s MWh (within 4 per cent) against %s billed at deemed "
      "kWh; technical losses %s MWh on APT-3, %s on APT-4 (each within 7 per cent) and %s on the fourteen feeders "
      "(within 4 per cent); non-technical loss %s." % (
          n1(r2["NTH-4 metered use, twelve months"]), n1(r2["NTH-3 metered use, twelve months"]),
          n1(r3["real use"]), n1(r3["deemed kWh billed"]), n1(r4["APT-3"]), n1(r4["APT-4"]),
          n1(r4["fourteen feeders"]), "; ".join("%s %s MWh (%s to %s)" % (
              f, n1(v), n1(v - max(75.0, 0.09 * v)), n1(v + max(75.0, 0.09 * v))) for f, v in sorted(r5.items(),
                                                                                       key=lambda x: -x[1]))))
    r6 = T["R6_bridge"]
    a("4. Line loss bridge sheet: line loss %.2f per cent in the twelve months to September 2024 and %.2f per cent in "
      "the twelve months to September 2026 (each within 0.05); of the %.2f point rise, technical losses %+.2f points, "
      "non-technical losses %+.2f points and everything else %+.2f points (each within 0.10)." % (
          r6["line loss, twelve months to September 2024"], r6["line loss, twelve months to September 2026"],
          T["loss_change"], r6["technical losses, points"], r6["non-technical losses, points"],
          r6["everything else, points"]))
    a("5. 2027 sheet, the peak hourly demand each approved 2027 connection adds: %s (each within 5 per cent)." % (
      "; ".join("%s %s kW" % (k, n1(np_[k])) for k in apps)))
    r8 = T["R8_tech2027"]
    a("6. 2027 sheet, each feeder's 2027 technical losses: APT-4 %s MWh and APT-3 %s MWh (each within 7 per cent), "
      "%s MWh on the fourteen feeders (within 3 per cent)." % (n1(r8["APT-4"]), n1(r8["APT-3"]),
                                                              n1(r8["fourteen feeders"])))
    a("")
    a("## Critical Components")
    a("")
    a("1. Technical losses at the loads' 2026 positions: APT-3 **%s MWh** and the fourteen feeders **%s MWh** "
      "(%.2f per cent of their energy in), where the 2019 study's percentages give %s and %s." % (
          n1(r4["APT-3"]), n1(r4["fourteen feeders"]), T["tech_system_pct_26"], n1(T["careful_tech_apt3_26"]),
          n1(T["careful_tech_system_26"])))
    a("2. The switching log replayed on the network: NTH-4 served **%d** customers at the end of March 2026 and "
      "**%d** at the end of May, after the April 21 transfer; today's GIS puts %d on it in March." % (
          r2["NTH-4 customers, 31 March 2026"], r2["NTH-4 customers, 31 May 2026"], T["careful_nth4_cust_mar26"]))
    a("3. CHL-3's energy in rebuilt for the ice storm's missing hours from the Cherry Hill delivery point: **%s MWh** "
      "in January 2026 and **%s MWh** for the twelve months." % (n1(r1["CHL-3, January 2026"]),
                                                                  n1(r1["CHL-3, twelve months to September 2026"])))
    a("4. The rise in line loss from %.2f to %.2f per cent: technical losses **%+.2f points**, non-technical "
      "**%+.2f points**, everything else **%+.2f points**." % (
          r6["line loss, twelve months to September 2024"], r6["line loss, twelve months to September 2026"],
          r6["technical losses, points"], r6["non-technical losses, points"], r6["everything else, points"]))
    a("")
    a("## Step-by-Step")
    a("")
    a("1. Put the delivery point meters (hour ending, standard time) and the feeder breakers' historian (hour "
      "beginning, local clock, the November hour twice) on one hour grid, with the stuck APT-2 transducer of August "
      "2025 treated as missing; the breakers then tie to each substation's purchases less its transformer losses and "
      "station service wherever all of them reported.")
    a("2. Rebuilt every missing breaker hour from its substation's balance: CHL-3's telemetry was down from January "
      "23 to February 3, 2026, while it carried CHL-2's customers through the emergency tie, so January's energy in "
      "is %s MWh; carrying the gap at CHL-3's own average for the hour gives %s, and the twelve months %s against "
      "%s." % (n1(r1["CHL-3, January 2026"]), n1(T["careful_e_in_chl3_jan26"]),
               n1(r1["CHL-3, twelve months to September 2026"]), n1(T["careful_e_in_chl3_26"])))
    a("3. Replayed every switching order on the GIS network (the old OMS names through the July 2024 crosswalk and "
      "the pole tags), so each node has its feeder hour by hour: the April 21, 2026 transfer leaves NTH-4 with %d "
      "customers in March and %d in May, and NTH-4's meters recorded %s MWh in the twelve months where today's GIS "
      "gives %s (%s MWh of NTH-3's use)." % (
          r2["NTH-4 customers, 31 March 2026"], r2["NTH-4 customers, 31 May 2026"],
          n1(r2["NTH-4 metered use, twelve months"]), n1(T["careful_nth4_metered_26"]), n1(T["moved_metered_26"])))
    a("4. Spread each read period's kWh over its days by the substation's daily energy, an estimated read folded into "
      "the actual read that trues it up; the lights at their lamp's input watts and each month's burning hours "
      "used %s MWh against %s billed at deemed kWh." % (n1(r3["real use"]), n1(r3["deemed kWh billed"])))
    a("5. Technical losses: each month's metered load at each node of the tree that served it gives the feeder an "
      "equivalent resistance from the GIS segments at the study's conventions (single-phase taps at %s times, "
      "secondary at %.1f per cent of metered energy), times each hour's breaker current squared, with transformer "
      "core and copper losses from the register by vintage: APT-3 %s MWh, where the study's %.2f per cent of its "
      "2026 energy gives %s, because the cold store and a grow now sit at the end of its main." % (
          WORDS[T["single_phase_factor"]], T["secondary_pct"], n1(r4["APT-3"]), T["study_apt3_pct"],
          n1(T["careful_tech_apt3_26"])))
    a("6. Non-technical loss is energy in plus customers' exports, less their meters, the large power meters, the "
      "lights and technical losses: %s; the careful but hurried route (today's GIS, the gap at the average, the study's "
      "percentages) files %s and sweeps %s." % (
          ", ".join("%s %s" % (f, n0(ntl[f])) for f in sorted(ntl, key=lambda f: -ntl[f])[:6]),
          ", ".join("%s %s" % (f, n0(c[f])) for f in cs), ", ".join(cs)))
    a("7. The bridge: purchases at the delivery points and sales on bills issued in each window give %.2f and %.2f "
      "per cent, split into the substations, technical losses, non-technical losses, the lights and billing timing; "
      "technical losses take %+.2f points of the rise, where holding them at the study's percentage leaves "
      "%+.2f to theft." % (r6["line loss, twelve months to September 2024"],
                            r6["line loss, twelve months to September 2026"], r6["technical losses, points"],
                            T["careful_d_nontechnical"]))
    a("8. 2027: the connected grows' peak hourly demand from the interval meters is %.3f of the load they applied "
      "for and the cold store's %.3f, so the three approved connections add %s kW; their loads at the existing "
      "grows' hourly shape on today's network, with APT-3's main reconductored from March 15, 2027, give APT-4 %s MWh, "
      "APT-3 %s MWh and %s MWh on the fourteen feeders (the applied loads give %s on APT-4)." % (
          T["df_grow"], T["df_cold"], ", ".join(n1(np_[k]) for k in apps[:-1]) + " and " + n1(np_[apps[-1]]),
          n1(r8["APT-4"]), n1(r8["APT-3"]),
          n1(r8["fourteen feeders"]), n1(T["nameplate_tech27_apt4"])))
    a("")
    a("No other four survives. The same four come out with load placed by each node's twelve-month energy or with "
      "each read period spread evenly over its days, and under conductor resistance at 25 C, transformer losses "
      "%d per cent either way, burning hours %d per cent lower and substation losses %d per cent higher. Each "
      "shortcut lands on a different four: the study's percentages put %s, today's GIS puts %s, and the storm gap "
      "carried at the average puts %s; placing load by transformer rating is ruled out because every transformer's "
      "customers are metered." % (
          T["perturbation_pcts"][1], T["perturbation_pcts"][0], T["perturbation_pcts"][2],
          swap(fo, s, "technical losses at the 2019 study's percentage"), swap(fo, s, "today's GIS feeder"),
          swap(fo, s, "breaker gaps carried at the feeder's own average")))
    open(path, "w").write("\n".join(lines) + "\n")
