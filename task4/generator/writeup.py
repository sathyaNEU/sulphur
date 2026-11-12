"""figures.json and submission.md, from results.compute: every figure the four answer blocks state is emitted here
from the same object the golden files are written from, never typed."""
import json

import numpy as np

import analysis as A
import golden as GD
import params as P

NAMES = {k: P.PART[k]["name"] for k in A.PARTS}
PLURAL = {"SG": "starter-generators", "BRK": "brake assemblies", "BAV": "bleed air shutoff valves",
          "NWS": "nose wheel steering actuators", "BAT": "main batteries", "CPC": "cabin pressure controllers",
          "FLA": "flap drive actuators", "ADC": "air data computers", "WXR": "weather radar receiver-transmitters",
          "VHF": "VHF transceivers", "PEC": "propeller electronic controls", "PDT": "propeller de-ice timers",
          "HYP": "engine-driven hydraulic pumps", "FBP": "fuel boost pumps", "WHC": "windshield heat controllers",
          "FDU": "engine fire detection control units"}


def flat(G):
    fc, MC, H, Hw = G["fc"], G["MC"], G["H"], G["Hw"]
    why, cyc_ch, fh_ch, summer = GD.reasons(G)
    f = {}
    for k in A.PARTS:
        f["rem_%s" % k] = int(round(fc[k]["total"]))
        f["rem_lo_%s" % k] = int(np.floor(G["rem_band"][k][0]))
        f["rem_hi_%s" % k] = int(np.ceil(G["rem_band"][k][1]))
        f["p10_%s" % k] = int(MC[k]["p10"])
        f["p90_%s" % k] = int(MC[k]["p90"])
        f["need_%s" % k] = int(G["need"][k])
        f["need_lo_%s" % k], f["need_hi_%s" % k] = int(G["need_band"][k][0]), int(G["need_band"][k][1])
        f["pool_%s" % k] = int(P.POOL[k])
        f["change_%s" % k] = int(G["calls"][k]) if k in G["robust"] else 0
        f["hproj_%s" % k] = int(round(H[k]["proj"]))
        f["hneed_%s" % k] = int(H[k]["spares"])
        f["qproj_%s" % k] = int(round(G["qproj"][k]))
        f["installed_%s" % k] = P.FLEET_N * P.PART[k]["pos"]
    rob = G["robust"]
    f["buy_units"] = int(sum(G["calls"][k] for k in rob if rob[k][0] == "BUY"))
    f["cut_units"] = int(-sum(G["calls"][k] for k in rob if rob[k][0] == "CUT"))
    f["n_buy"] = sum(1 for k in rob if rob[k][0] == "BUY")
    f["n_cut"] = sum(1 for k in rob if rob[k][0] == "CUT")
    f["saving"] = int(round(G["saving"]))
    f["saving_lo"], f["saving_hi"] = int(np.floor(G["saving_band"][0])), int(np.ceil(G["saving_band"][1]))
    f["saving_face"] = int(round(Hw["face"]))
    f["saving_cf"] = int(round(Hw["cf_only"]))
    f["saving_eb"] = int(round(G["saving_eb"]))
    f["n_listed"] = int(len(G["W"]))
    f["n_scrap"] = int(len(G["scrap"]))
    f["n_cf_set"] = int(len(Hw["cf_set"]))
    f["cyc_ch_pct"] = int(round(cyc_ch * 100))
    f["fh_ch_pct"] = int(round(-fh_ch * 100))
    for k in P.IN_HOUSE:
        f["tat_summer_%s" % k] = int(round(summer.get(k, 0.0)))
        f["tat_2026_%s" % k] = int(round(H[k]["tat"]))
    allsum = [t for k, m, t, rep in G["tat_in"] if m in (7, 8)]
    f["tat_summer"] = int(round(float(np.mean(allsum))))
    f["tat_2026"] = int(round(float(np.mean([H[k]["tat"] for k in P.IN_HOUSE]))))
    sp = fc["PEC"]["split"]
    f["pec_cut_pct"] = int(round((1 - sp["rate_mod"] / sp["rate_un"]) * 100))
    f["pec_mod_now_pct"] = int(round(sp["mod_installed"] / sp["installed"] * 100))
    f["gap_SG"] = round(2 * G["D"]["SG"]["ll_gap"], 1)
    f["gap_BRK"] = round(2 * G["D"]["BRK"]["ll_gap"], 1)
    f["gap_BAV"] = round(2 * G["D"]["BAV"]["ll_gap"], 1)
    f["scrap_list"] = ", ".join(G["scrap"])
    f["scrap_set"] = list(G["scrap"])
    f["call"] = list(G["call_set"])
    f["call_units"] = {k: int(G["calls"][k]) for k in sorted(G["robust"])}
    f["fill_pct"], f["range_pct"], f["window_days"] = 95, 80, 120
    f["pn"] = {k: P.PART[k]["pn"] for k in A.PARTS}
    f["rem"] = {k: f["rem_%s" % k] for k in A.PARTS}
    f["rem_cyc"] = {k: f["rem_%s" % k] for k in ("SG", "BRK", "BAV")}
    f["need"] = {k: f["need_%s" % k] for k in A.PARTS}
    f["need_inhouse"] = {k: f["need_%s" % k] for k in P.IN_HOUSE}
    f["pec"] = {"removals": f["rem_PEC"], "spares": f["need_PEC"]}
    f["range"] = {**{k + "_lo": f["p10_%s" % k] for k in A.PARTS}, **{k + "_hi": f["p90_%s" % k] for k in A.PARTS}}
    f["why"] = why
    return f


def write_figures(path, f):
    json.dump(f, open(path, "w"), indent=1, ensure_ascii=False)


def _line(f, k):
    return ("%s %s: %d expected unscheduled removals (band %d to %d), 80 per cent range %d to %d"
            % (P.PART[k]["pn"], NAMES[k], f["rem_%s" % k], f["rem_lo_%s" % k], f["rem_hi_%s" % k],
               f["p10_%s" % k], f["p90_%s" % k]))


def _need(f, k):
    lo, hi = f["need_lo_%s" % k], f["need_hi_%s" % k]
    band = ("%d" % lo) if lo == hi else ("%d to %d" % (lo, hi))
    ch = f["change_%s" % k]
    act = ("buy %d" % ch) if ch > 0 else (("cut %d" % -ch) if ch < 0 else "hold")
    return "%s %s: needs %d (band %s) against %d held, %s" % (P.PART[k]["pn"], NAMES[k], f["need_%s" % k], band,
                                                              f["pool_%s" % k], act)


def submission(f, G):
    rob = G["robust"]
    buys = [k for k in A.PARTS if k in rob and rob[k][0] == "BUY"]
    cuts = [k for k in A.PARTS if k in rob and rob[k][0] == "CUT"]
    holds = [k for k in A.PARTS if k not in rob]

    def items(ks):
        return ", ".join("%s %d" % (PLURAL[k], abs(f["change_%s" % k])) for k in ks)
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics.  ")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## Final Recommendation\n")
    L.append("**Buy %d rotable spares for 2027 (%s) and cut %d (%s), and withdraw only the %d watch-list serials whose "
             "removals follow the serial.** Palm's formula on October's MTBUR and the 2026 average turnaround would "
             "stock %d starter-generators and %d brake assemblies where the plan needs %d and %d, because it carries landing-driven wear on flight hours "
             "that fall %d per cent in 2027 while landings rise %d per cent and misses the Bodø shop's summer queue of about "
             "%d days against %d, and withdrawing all %d listed serials saves about %d removals a year, not the %d their "
             "counts suggest.\n"
             % (f["buy_units"], items(buys), f["cut_units"], items(cuts), f["n_scrap"], f["hneed_SG"], f["hneed_BRK"],
                f["need_SG"], f["need_BRK"], f["fh_ch_pct"], f["cyc_ch_pct"], f["tat_summer"], f["tat_2026"], f["n_listed"], f["saving"],
                f["saving_face"]))
    L.append("## Supplementary Questions\n")
    L.append("### %s\n" % GD.XLSX)
    L.append("1. The Spares plan 2027 sheet has one row per part number, sixteen in all, in the stores' order, with the "
             "part number, description, installed positions, pool today, expected 2027 unscheduled removals, the 80 per "
             "cent range's low and high, the spares needed, the change, the action and what moves the line. Expected "
             "removals and ranges, whole removals:")
    for k in A.PARTS:
        L.append("   - %s." % _line(f, k))
    L.append("2. Spares needed for the 95 per cent fill rate, whole units:")
    for k in A.PARTS:
        L.append("   - %s." % _need(f, k))
    L.append("3. The change against what the pool holds today: buy %d (%s), cut %d (%s); hold %s.\n"
             % (f["buy_units"], items(buys), f["cut_units"], items(cuts), ", ".join(PLURAL[k] for k in holds)))
    L.append("### %s\n" % GD.PPTX)
    why = f["why"]
    L.append("4. The lines to buy and to cut, a slide each for the plan, the landing-driven parts, the Bodø shop, the "
             "watch list and the cuts, with what moves each:")
    for k in buys + cuts:
        L.append("   - %s %s %d: %s." % ("Buy" if k in buys else "Cut", PLURAL[k], abs(f["change_%s" % k]), why[k]))
    L.append("5. Withdrawing every serial on the October watch list saves about %d unscheduled removals a year (band %d "
             "to %d), counted for each position over the year with another unit fitted while a serial is away for repair."
             % (f["saving"], f["saving_lo"], f["saving_hi"]))
    L.append("6. Withdraw %d of the %d listed serials: %s.\n" % (f["n_scrap"], f["n_listed"], f["scrap_list"]))
    L.append("## Critical Components\n")
    L.append("1. The starter-generators, brakes and bleed valves fail by landings and starts, not flight hours: "
             "**%d, %d and %d** expected 2027 removals against %d, %d and %d at October's MTBUR on 2027's flight hours, with landings "
             "**%d per cent** up and flight hours **%d per cent** down."
             % (f["rem_SG"], f["rem_BRK"], f["rem_BAV"], f["qproj_SG"], f["qproj_BRK"], f["qproj_BAV"], f["cyc_ch_pct"], f["fh_ch_pct"]))
    L.append("2. The Bodø shop's queue runs about **%d days** in July and August 2027 against a 2026 average of %d, so "
             "the in-house lines need **%d, %d, %d, %d and %d** starter-generators, brakes, bleed valves, nose wheel steering "
             "actuators and batteries." % (f["tat_summer"], f["tat_2026"], f["need_SG"], f["need_BRK"], f["need_BAV"],
                                            f["need_NWS"], f["need_BAT"]))
    L.append("3. Of the %d watch-list serials, **%d** have removals that follow the serial; withdrawing the whole list "
             "saves about **%d** removals a year." % (f["n_listed"], f["n_scrap"], f["saving"]))
    L.append("4. SB 61-0042 cuts the propeller control's confirmed failures by about %d per cent and spreads with every "
             "removal, so the line expects **%d** removals in 2027 and needs **%d** of the %d it holds."
             % (f["pec_cut_pct"], f["rem_PEC"], f["need_PEC"], f["pool_PEC"]))
    L.append("")
    L.append("## Step-by-Step\n")
    L.append("1. Cleaned component_changes_2023-01_2026-11.csv (corrected entries superseding the originals, the S/N "
             "prefix of 2024's scanners, the two reason vocabularies) and matched each unscheduled removal to its order in "
             "bodo_shop_work_orders_2023-2026.csv or vendor_repair_orders_2023-2026.xlsx for its finding and its return.")
    L.append("2. Built each aircraft-month's landings and flight hours from flight_legs_2023-01_2026-11.csv (the re-sent "
             "days dropped, air time from block less the field's taxi where the off and on times are missing), its base "
             "from fleet_register.xlsx and its frost from station_weather_daily_2023-2026.csv.")
    L.append("3. Fitted each part's confirmed failures on landings, flight hours and calendar days in turn: the "
             "starter-generator, brake and bleed valve follow landings, the record's bases flying sectors of very "
             "different length (twice the log-likelihood gap %.1f, %.1f and %.1f); the October report's MTBUR, carried to "
             "2027's flight hours, gives %d, %d and %d." % (f["gap_SG"], f["gap_BRK"], f["gap_BAV"], f["hproj_SG"],
                                                             f["hproj_BRK"], f["hproj_BAV"]))
    L.append("4. Took 2027's landings and flight hours from flying_programme_2027.xlsx, the Helgeland routes from 1 April "
             "flown on sectors of about a quarter of an hour: landings %d per cent up, flight hours %d per cent down, so "
             "the landing-driven parts expect %d, %d and %d removals." % (f["cyc_ch_pct"], f["fh_ch_pct"], f["rem_SG"],
                                                                        f["rem_BRK"], f["rem_BAV"]))
    L.append("5. Rebuilt each propeller control's installed spells and its SB 61-0042 date from the repairers' returns: "
             "the modified units fail about %d per cent less, %d per cent of the installed units carried the bulletin at the "
             "snapshot and every removal converts another, so 2027 expects %d removals and the line needs %d of the %d it "
             "holds; October's MTBUR on 2027's hours gives %d." % (f["pec_cut_pct"], f["pec_mod_now_pct"],
                                                                           f["rem_PEC"], f["need_PEC"], f["pool_PEC"],
                                                                           f["qproj_PEC"]))
    L.append("6. Put the no-fault-found removals at each station's own rate on the 2027 base mix, with more flying based "
             "at Bodø, where troubleshooting finds the aircraft's faults before units are swapped, and the flight-hour "
             "parts on 2027's %d per cent fewer hours: the air data computer expects %d removals, the VHF transceiver %d "
             "and the windshield heat controller %d." % (f["fh_ch_pct"], f["rem_ADC"], f["rem_VHF"], f["rem_WHC"]))
    L.append("7. Replayed the Bodø shop day by day on its roster with its capacity set so the replay reproduces its own "
             "2024 to 2026 turnarounds, then fed it 2027's removals: about %d days in July and August against a 2026 "
             "average of %d, which the average-turnaround route never sees." % (f["tat_summer"], f["tat_2026"]))
    L.append("8. Replayed each part's pool through 2027 (each removal's return from the shop replay or the repairer's own "
             "turnaround, the winters on record, the no-fault-found months' spread) and read the fewest spares giving a "
             "95 per cent fill rate: the starter-generator needs %d and the brake %d, where Palm's formula on the average "
             "turnaround gives %d and %d." % (f["need_SG"], f["need_BRK"], f["hneed_SG"], f["hneed_BRK"]))
    L.append("9. Read the watch list serial by serial: removals its aircraft drove (three or more found serviceable from "
             "one position inside 120 days, two or more serials) set aside, each serial's own removals over its own "
             "installed exposure, the part's serials as two groups: %d of %d serials are worth withdrawing and the whole "
             "list saves about %d; the counts at face value say %d, the confirmed failures alone %d, one shrinkage "
             "toward the part's rate %d." % (f["n_scrap"], f["n_listed"], f["saving"], f["saving_face"], f["saving_cf"],
                                            f["saving_eb"]))
    L.append("10. Set each line's spares against its pool: buy %d on %d lines and cut %d on %d.\n"
             % (f["buy_units"], f["n_buy"], f["cut_units"], f["n_cut"]))
    L.append("No other plan survives the files: a per-flight-hour rate is rejected by the bases' own landings, which the "
             "starter-generator, brake and bleed valve failures follow; the 2026 average turnaround is rejected by the "
             "shop's own queue, which the replay reproduces before it carries 2027's load; the propeller control's 2026 "
             "rate is rejected by the repairers' bulletin dates; and the watch list's counts are rejected by the removals "
             "each serial's aircraft drove and by each serial's own record, which a single shrinkage toward the part's "
             "rate pulls in too far.")
    return "\n".join(L) + "\n"
