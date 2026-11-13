"""task22 architecture 2 (redesigned after the review of 2026-11-13): submission.md, the four answer blocks, every
figure read from figures.json."""
import params as P

CAREFUL = "the careful but hurried route (all three)"
C1 = "every fall in use booked as gas taken without authorization (the dual-fuel homes aside)"
C2 = "every lost heating response booked as a furnace tap, no cold-day test"
C3 = "every corrector's volume taken as recorded"
NODIV = "no gas taken without authorization subtracted"
ALLF = "every fall in use booked as gas taken without authorization (rebated homes aside)"


def _f(x, d=0):
    return ("{:,.%df}" % d).format(x)


def _join(xs):
    xs = list(xs)
    if not xs:
        return "none"
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def write(figs, E, path):
    x = figs["_extra"]
    lt = x["leak_table"]
    g, c = lt["golden"], lt["careful"]
    des, cho = figs["R4_designated"], figs["R6_changeout"]
    r1, r2, r3, r5 = figs["R1_basis"], figs["R2_unauthorized"], figs["R3_leak_pct"], figs["R5_unauthorized_mcf"]
    sc = x["shortcut_sets"]
    careful = x["careful_designated"]
    bd = x["basis"]["districts"]
    st = x["basis"]["stations"]
    pto = [s for s in st if s["corrector"] == "EVC-I"]
    ptz = [s for s in st if s["corrector"] == "EVC-II"]
    col = x["collapses"]
    tp = x["tpar"]
    b = x["bands_stated"]
    rs_in, rs_rec = bd["Riverside"]["gas_in_real"], bd["Riverside"]["gas_in_recorded"]
    ei_ev, ei_rec = bd["East Industrial"]["corrector_real"], bd["East Industrial"]["corrector_recorded"]
    bt = x["basis_totals"]
    ev_all, ev_gap, st_gap, ei_gap = bt["corrector_total"], bt["corrector_gap"], bt["station_gap"], bt["ei_gap"]
    k_rs, k_ch, k_ei = ("Riverside, gas in, twelve months to September 2026",
                        "College Hill, gas in, twelve months to September 2026",
                        "East Industrial, corrector customers, twelve months to September 2026")
    k_lv = "Lakeview, gas in, December 2025"
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
      "loss in the twelve months to September 2026 was %s to %s per cent of their gas in (Riverside %s, Lakeview %s, "
      "Sundquist %s). Reject the list (%s) that every corrector's own volume and every fall in use booked as theft "
      "give (East Industrial %s, Riverside %s, Lakeview %s, Sundquist %s): four regulator station correctors and every "
      "customer corrector leave the gas's supercompressibility out, which puts East Industrial over the line and "
      "pulls Riverside down, and the falls in Lakeview, Sundquist and Riverside were households away for the winter "
      "and dual-fuel heat pumps, which took no gas."
      % (_join(des), _join(cho), _f(min(g[d] for d in des), 2), _f(max(g[d] for d in des), 2),
         _f(r3["Riverside"], 2), _f(r3["Lakeview"], 2), _f(r3["Sundquist"], 2), _join(careful),
         _f(c["East Industrial"], 2), _f(c["Riverside"], 2), _f(c["Lakeview"], 2), _f(c["Sundquist"], 2)))
    A("")
    A("## Supplementary Questions")
    A("")
    A("### bpu_district_gas_balance_2023-10_2026-09.xlsx")
    A("")
    A("1. Monthly balance sheet: %d rows, one per district and month from October 2023 to September 2026, Mcf at "
      "base conditions on one real-gas basis, with gas in at the regulator stations, the billed volume of the "
      "cycle-read meters carried to the calendar month, what the meters without temperature compensation "
      "under-registered, the corrector customers' gas at base conditions, own use, third-party damage, gas taken "
      "without authorization and the leak loss left. Gas in: Lakeview %s Mcf in December 2025 (within %s per cent); "
      "Riverside %s Mcf and College Hill %s Mcf in the twelve months to September 2026 (each within %s per cent). "
      "Corrector customers: East Industrial %s Mcf in the twelve months (within %s per cent)."
      % (figs["monthly_rows"], _f(r1[k_lv], 1), _f(b["month_pct"], 1), _f(r1[k_rs]), _f(r1[k_ch]),
         _f(b["year_pct"], 1), _f(r1[k_ei]), _f(b["year_pct"], 1)))
    A("2. Twelve months to September 2026 sheet, one row per district: the balance's parts, leak loss as a share of "
      "gas in, the meters without compensation and their under-registration as a share of their billed volume, and "
      "the two decisions. Leak loss as a share of gas in: %s (each within %s points). The main replacement program "
      "(Rule 1) takes %s; the 2027 meter changeout (Rule 2) goes to %s."
      % ("; ".join("%s %s" % (k, _f(v, 2)) for k, v in r3.items()), _f(b["share_pts"], 2), _join(des), _join(cho)))
    A("3. Without authorization sheet, one row per premise: the premise, its district, the account or accounts that "
      "held it from the month its use fell, the finding (bypass or furnace tap), that month and the gas taken. %d "
      "premises and %d accounts (each within %d); gas taken %s (each within %s per cent)."
      % (r2["premises"], r2["accounts"], b["count"],
         "; ".join("%s %s" % (k.replace(", Mcf", ""), _f(v) + " Mcf") for k, v in r5.items()), _f(b["mcf_pct"])))
    A("")
    A("### lauf_program_2027_commission.pptx")
    A("")
    A("4. A short deck for the Commission: the main replacement districts and the changeout districts on its first "
      "slide, a bar chart of the fourteen districts' leak loss with the %s above the 1.0 per cent line in blue, the "
      "reported loss's parts on the real-gas basis, and a bar chart of the under-registration by district with the "
      "%s changeout districts in blue." % (WORDS[len(des)], WORDS[len(cho)]))
    A("")
    A("## Critical Components")
    A("")
    A("1. On one real-gas basis: the four EVC-I station correctors (%s) and every customer corrector correct for "
      "pressure and temperature only; Riverside's gas in was **%s** Mcf in the twelve months, not the %s its corrector "
      "recorded, and East Industrial's corrector customers took **%s** Mcf, %s more than their correctors bill."
      % (_join(s["station"] for s in pto), _f(rs_in), _f(rs_rec), _f(ei_ev), _f(ei_gap)))
    A("2. Gas taken without authorization: **%d** premises (**%d** accounts), %d bypasses and %d furnace taps; the "
      "%d households away for the winter and the %d dual-fuel heat pumps whose use also fell took none."
      % (r2["premises"], r2["accounts"], col["bypasses"], col["furnace_taps"], col["absences"], col["dual_fuel"]))
    A("3. Leak loss in the twelve months to September 2026: Riverside **%s**, Lakeview **%s**, Sundquist **%s** per "
      "cent of gas in, above the 1.0 per cent line; East Industrial **%s** and Halvorsen **%s**, below it."
      % (_f(r3["Riverside"], 2), _f(r3["Lakeview"], 2), _f(r3["Sundquist"], 2), _f(r3["East Industrial"], 2),
         _f(r3["Halvorsen"], 2)))
    A("")
    A("## Step-by-Step")
    A("")
    A("1. Rebuilt each regulator station's faulty gas days from the city gate less the other stations (Riverside's "
      "January 12 to 25 communication gap, Lakeview's December transducer failure, Westgate's stuck temperature "
      "transmitter); Lakeview's December 2025 gas in is %s Mcf." % _f(r1[k_lv], 1))
    A("2. Set each station corrector's corrected-to-uncorrected ratio against its pressure-and-temperature factor "
      "(atmospheric %s psia, solved from the customer correctors' own ratios): the %d EVC-II units run %s to %s above "
      "it, the gas's supercompressibility at their pressure, the %s EVC-I units at %s. Put the EVC-I stations on the "
      "EVC-II basis with Dranchuk and Abou-Kassem on the gate's specific gravity, which the EVC-II stations' own "
      "records reproduce: Riverside's twelve months are %s Mcf against %s recorded, and %s Mcf across the fourteen "
      "districts."
      % (_f(x["p_atm"], 2), len(ptz), _f(bt["ptz_factor_min"], 4), _f(bt["ptz_factor_max"], 4),
         WORDS[len(pto)], _f(bt["pt_factor_mean"], 4), _f(rs_in), _f(rs_rec), _f(st_gap)))
    A("3. Every customer corrector's ratio is its pressure-and-temperature factor exactly, so the process customers "
      "at 25 to 58 psig are billed short of their gas at base conditions: the corrector customers took %s Mcf in the "
      "twelve months, %s more than billed, %s of it in East Industrial."
      % (_f(ev_all), _f(ev_gap), _f(ei_gap)))
    A("4. Turned the AMR reads into actual-to-actual periods per meter, carried them to months on each district's "
      "daily sendout, and corrected the meters without temperature compensation with the gas temperature the loggers "
      "tie to the soil at 20 inches (plus %s of the air's difference from it) and indoors to the basement's."
      % _f(tp.get("k", 0), 3))
    A("5. Took each premise's monthly use against its own weather response the year before: %d fell for three months "
      "or more into the heating season outside a vacancy or an exchange. %d lost their summer base load too "
      "(bypasses). %d were back at their own weather response in May 2026 (away for the winter). Of the rest, read "
      "period by read period against the degree days of the cold days only, %d took their whole past heating slope "
      "on the coldest days (dual-fuel heat pumps), and %d more have a dual-fuel controls rebate on file. %s over "
      "the spring. That leaves %d furnace taps: %d premises, %d accounts. Booking every fall instead counts %d premises "
      "and puts Lakeview at %s and Sundquist at %s; booking the dual-fuel homes as taps puts Riverside at %s and "
      "Sundquist at %s."
      % (col["total"], col["bypasses"], col["absences"], col["dual_fuel_test"], col["dual_fuel_rebated"],
         ("%d premises changed hands" % col["turnover"]) if col["turnover"] != 1 else "One premise changed hands",
         col["furnace_taps"], r2["premises"], r2["accounts"], x["booked_every_fall_golden_path"],
         _f(lt[ALLF]["Lakeview"], 2), _f(lt[ALLF]["Sundquist"], 2), _f(lt[C2]["Riverside"], 2),
         _f(lt[C2]["Sundquist"], 2)))
    A("6. Leak loss is gas in less the billed volume, the under-registration, the corrector customers at base "
      "conditions, own use, the damage reports and the gas taken without authorization: %s. The careful but hurried "
      "route (every corrector as recorded, every fall booked) leaves %s over the line."
      % ("; ".join("%s %s" % (k, _f(v, 2)) for k, v in g.items()), _join(careful)))
    A("7. Rule 2 on the under-registration: %s exceed 3.5 per cent of the volume billed for their meters without "
      "compensation with 100 or more such meters; Westgate and Heritage Park have fewer than 100." % _join(cho))
    A("")
    A("No other set survives. The same %s districts come out under every variant of the modelled steps (%d of them: "
      "supercompressibility from Dranchuk and Abou-Kassem, Hall and Yarborough or the EVC-II stations' own fit, each "
      "read period spread on the sendout or a degree-day fit, the gas temperature tied to the soil or to the "
      "commercial correctors), under each convention of the screen and each input moved 20 per cent either way. Each "
      "shortcut lands on another list: correctors as recorded on %s; every fall booked on %s; the dual-fuel homes as "
      "taps on %s; no gas taken without authorization subtracted on %s."
      % (WORDS[len(des)], E["battery"]["count"], _join(sc[C3]), _join(sc[C1]), _join(sc[C2]), _join(sc[NODIV])))
    open(path, "w").write("\n".join(lines) + "\n")
