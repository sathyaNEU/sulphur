"""figures.json and submission.md, from results.compute: every figure the four answer blocks, the workbook and the
note state is emitted here from one object, never typed. Kegs are stated to the nearest ten."""
import json

import numpy as np

import params as P

SIZES = (50, 30, 20)


def r10(x):
    return int(round(float(x) / 10.0) * 10)


def band(vals, pad=0.03, step=10):
    lo, hi = min(vals) * (1 - pad), max(vals) * (1 + pad)
    return int(np.floor(lo / step) * step), int(np.ceil(hi / step) * step)


def flat(G):
    g = G["golden"]
    fam = list(G["family"].values())
    per = G.get("perturbed", {})
    f = {}
    yl = g["_yl"]
    for s in SIZES:
        f["register_%d" % s] = int(G["register"][s])
        f["fleet_%d" % s] = r10(g["fleet"][s])
        f["untraced_%d" % s] = f["register_%d" % s] - f["fleet_%d" % s]
        f["loss_%d" % s] = r10(g["loss"][s])
        f["sent_%d" % s] = int(yl["sent"][s])
        f["back_%d" % s] = int(yl["back"][s])
        f["out1_%d" % s] = r10(yl["out1"][s])
        f["out2_%d" % s] = r10(yl["out2"][s])
        f["gate_%d" % s] = int(G["gate_loss"][s])
        f["deliv_%d" % s] = r10(g["deliv"][s])
        f["deliv_lo_%d" % s] = r10(g["deliv_lo"][s])
        f["deliv_hi_%d" % s] = r10(g["deliv_hi"][s])
        f["deliv_week_%d" % s] = str(g["deliv_week"][s].date())
        f["week_%d" % s] = str(g["week"][s].date())
        f["lost_to_week_%d" % s] = r10(g["lost_to_week"][s])
        f["have_%d" % s] = r10(g["have"][s])
        f["float_%d" % s] = r10(g["float"][s])
        f["need_%d" % s] = r10(g["need"][s])
        f["circ_%d" % s] = r10(g["need"][s] - g["float"][s])
        parts = g["need_parts"][s]
        f["part_existing_%d" % s] = r10(parts["existing"])
        f["part_new_%d" % s] = r10(parts["new_lines"])
        f["part_pipe_%d" % s] = r10(parts["new_pipe"])
        f["part_store_%d" % s] = r10(parts["foundry_store"])
        f["buy_%d" % s] = r10(g["buy"][s])
        f["elasticity_%d" % s] = round(float(g["elasticity"][s]), 2)
        # bands: the golden family's spread (and the perturbations for the order), with a small margin
        f["loss_lo_%d" % s], f["loss_hi_%d" % s] = band([g["loss"][s]] + [G["family"][k]["loss"][s] for k in (
            "the tagged share of fills taken over the last 60 days",
            "the tagged kegs scaled by their share of the register's active kegs")], pad=0.10)
        f["fleet_lo_%d" % s], f["fleet_hi_%d" % s] = band([x["fleet"][s] for x in fam] + [g["fleet"][s]], pad=0.02)
        f["deliv_band_lo_%d" % s], f["deliv_band_hi_%d" % s] = band([g["deliv"][s]], pad=0.05)
        f["need_lo_%d" % s], f["need_hi_%d" % s] = band([x["need"][s] for x in fam] + [g["need"][s]], pad=0.025)
        f["buy_lo_%d" % s], f["buy_hi_%d" % s] = band([x["buy"][s] for x in fam] + [g["buy"][s]], pad=0.06, step=50)
    for s in (50, 30):
        f["estate_%d" % s] = r10(g["estate"][s])
        f["estate_lo_%d" % s], f["estate_hi_%d" % s] = band([x["estate"][s] for x in fam] + [g["estate"][s]], pad=0.03)
    f["store"] = r10(g["store"])
    f["store_lo"], f["store_hi"] = band([g["store"]] + [x["store"] for x in fam], pad=0.04)
    f["pubs"] = len(G["F"]["plan"]["Maplestead pubs"].pub.unique()) if "F" in G else 300
    f["rec"] = ("Order %s fifty-litre, %s thirty-litre and %s twenty-litre kegs by 18 December for the April delivery. "
                "The keg register's %s, %s and %s active kegs overstate the fleet by about %s, %s and %s kegs lost "
                "in the trade since the November 2023 reconciliation, and the Maplestead pubs' slow 30 litre lines and the "
                "widened Foundry range each need far more kegs than their volumes at the fleet's usual turns suggest."
                % (_c(f["buy_50"]), _c(f["buy_30"]), _c(f["buy_20"]), _c(f["register_50"]), _c(f["register_30"]),
                   _c(f["register_20"]), _c(f["untraced_50"]), _c(f["untraced_30"]), _c(f["untraced_20"])))
    f["note_fleet"] = ("The register still lists every keg that has gone missing since it was last reconciled. Counting "
                       "what is on our sites at the stocktake and what the tagged kegs show is out with customers, the "
                       "fleet at 30 November is %s, %s and %s kegs. The trade lost %s, %s and %s kegs in the year to "
                       "November, once the other brewers' kegs the drivers bring back with ours are taken out of the "
                       "empties and our kegs coming back through the exchange and the recovery agent are counted in."
                       % (_c(f["fleet_50"]), _c(f["fleet_30"]), _c(f["fleet_20"]), _c(f["loss_50"]), _c(f["loss_30"]),
                          _c(f["loss_20"])))
    f["note_new"] = ("A pub line holds a keg on tap and its delivery cover whatever it sells, so the Maplestead pubs' "
                     "lines, slow on 30 litre, will hold about %s fifty-litre and %s thirty-litre kegs in the busiest week. The 2027 "
                     "Foundry range is brewed in 200-keg lots across up to 18 beers, so the cold store will hold about "
                     "%s full kegs in the twenty-litre busiest week."
                     % (_c(f["estate_50"]), _c(f["estate_30"]), _c(f["store"])))
    f["note_range"] = ("At normal weather the busiest delivery week sends out about %s, %s and %s kegs (80 per cent "
                       "ranges %s to %s, %s to %s and %s to %s over the last ten summers). The order holds for each "
                       "size across the methods we tried, within %s to %s, %s to %s and %s to %s kegs. Normal weather is a smoothed "
                       "average day, so its busiest week sits at the low end of the range real summers give: a real "
                       "summer's hot week lifts its peak above the average's."
                       % (_c(f["deliv_50"]), _c(f["deliv_30"]), _c(f["deliv_20"]), _c(f["deliv_lo_50"]),
                          _c(f["deliv_hi_50"]), _c(f["deliv_lo_30"]), _c(f["deliv_hi_30"]), _c(f["deliv_lo_20"]),
                          _c(f["deliv_hi_20"]), _c(f["buy_lo_50"]), _c(f["buy_hi_50"]), _c(f["buy_lo_30"]),
                          _c(f["buy_hi_30"]), _c(f["buy_lo_20"]), _c(f["buy_hi_20"])))
    return f


def _c(x):
    return "{:,}".format(int(x))


def write_figures(path, f):
    import effort_passes as EP
    out = {k: v for k, v in f.items() if not k.startswith(("rec", "note_"))}
    out.update(EP.composite(f))
    json.dump(out, open(path, "w"), indent=1)


def submission(f, G):
    c = _c
    h = G["hurried"]
    car = G["careful"]
    L = []
    L.append("# Final Recommendation\n")
    L.append("Order %s new 50 litre kegs, %s new 30 litre kegs and %s new 20 litre kegs by 18 December 2026 for the "
             "April 2027 delivery, rejecting the register's count of the fleet (which would order no 50 litre kegs at "
             "all) and the fleet's average keg turns for the Maplestead pubs and the 2027 Foundry range (which would "
             "order about %s fewer 30 litre and %s fewer 20 litre kegs).\n"
             % (c(f["buy_50"]), c(f["buy_30"]), c(f["buy_20"]),
                c(f["buy_30"] - int(round(h["estate_turns"]["buy"][30], -1))),
                c(f["buy_20"] - int(round(h["store_cover"]["buy"][20], -1)))))
    L.append("# Supplementary Questions\n")
    L.append("Every figure is in kegs, stated to the nearest ten, for 50, 30 and 20 litre kegs in that order. The "
             "spreadsheet carries one sheet for the order's bridge by size and one for each figure below with its "
             "workings; the note is one or two pages with the order, the table and the reasons.\n")
    L.append("1. Kegs to buy: %s, %s and %s (accepted %s to %s, %s to %s and %s to %s)."
             % (c(f["buy_50"]), c(f["buy_30"]), c(f["buy_20"]), c(f["buy_lo_50"]), c(f["buy_hi_50"]),
                c(f["buy_lo_30"]), c(f["buy_hi_30"]), c(f["buy_lo_20"]), c(f["buy_hi_20"])))
    L.append("2. Kegs lost in the trade in the twelve months to 30 November 2026: %s, %s and %s (accepted %s to %s, "
             "%s to %s and %s to %s). The depot gate counters' fulls out less empties in (%s, %s and %s) is not the "
             "loss: the empties include other brewers' kegs, and own kegs come back through the exchange and the "
             "recovery agent without passing a gate."
             % (c(f["loss_50"]), c(f["loss_30"]), c(f["loss_20"]), c(f["loss_lo_50"]), c(f["loss_hi_50"]),
                c(f["loss_lo_30"]), c(f["loss_hi_30"]), c(f["loss_lo_20"]), c(f["loss_hi_20"]), c(f["gate_50"]),
                c(f["gate_30"]), c(f["gate_20"])))
    L.append("3. Usable kegs at 30 November 2026: %s, %s and %s (accepted %s to %s, %s to %s and %s to %s), against "
             "the register's %s, %s and %s active kegs."
             % (c(f["fleet_50"]), c(f["fleet_30"]), c(f["fleet_20"]), c(f["fleet_lo_50"]), c(f["fleet_hi_50"]),
                c(f["fleet_lo_30"]), c(f["fleet_hi_30"]), c(f["fleet_lo_20"]), c(f["fleet_hi_20"]),
                c(f["register_50"]), c(f["register_30"]), c(f["register_20"])))
    L.append("4. The most kegs delivered in one week of the 2027 season at normal weather: %s, %s and %s (each "
             "accepted within 5 per cent), with 80 per cent ranges over the 2016 to 2025 summers of %s to %s, %s to "
             "%s and %s to %s (each end within 5 per cent). Normal weather is a smoothed average day, so its busiest "
             "week sits at the low end of the range: each real summer's hot spell lifts its own peak."
             % (c(f["deliv_50"]), c(f["deliv_30"]), c(f["deliv_20"]), c(f["deliv_lo_50"]), c(f["deliv_hi_50"]),
                c(f["deliv_lo_30"]), c(f["deliv_hi_30"]), c(f["deliv_lo_20"]), c(f["deliv_hi_20"])))
    L.append("5. Kegs held at the %d Maplestead pubs in the busiest week: %s fifty-litre (accepted %s to %s) and %s "
             "thirty-litre (accepted %s to %s)."
             % (f["pubs"], c(f["estate_50"]), c(f["estate_lo_50"]), c(f["estate_hi_50"]), c(f["estate_30"]),
                c(f["estate_lo_30"]), c(f["estate_hi_30"])))
    L.append("6. Full Foundry kegs in the Brighouse cold store in the 20 litre busiest week (week ending %s): %s "
             "(accepted %s to %s)." % (f["week_20"], c(f["store"]), c(f["store_lo"]), c(f["store_hi"])))
    L.append("7. Kegs needed in circulation in each size's busiest week, with the washer's float: %s, %s and %s "
             "(accepted %s to %s, %s to %s and %s to %s); the busiest weeks end %s, %s and %s.\n"
             % (c(f["need_50"]), c(f["need_30"]), c(f["need_20"]), c(f["need_lo_50"]), c(f["need_hi_50"]),
                c(f["need_lo_30"]), c(f["need_hi_30"]), c(f["need_lo_20"]), c(f["need_hi_20"]), f["week_50"],
                f["week_30"], f["week_20"]))
    L.append("# Critical Components\n")
    L.append("1. The usable fleet is the kegs on site at the stocktake plus the kegs out with customers that will come "
             "back, %s, %s and %s, not the register's %s, %s and %s: the register keeps every keg lost since the "
             "November 2023 reconciliation as active."
             % (c(f["fleet_50"]), c(f["fleet_30"]), c(f["fleet_20"]), c(f["register_50"]), c(f["register_30"]),
                c(f["register_20"])))
    L.append("2. The year's loss is %s, %s and %s kegs once the empties are counted at the washer (another brewer's "
             "kegs rejected there) and the kegs out in the trade at both stocktakes are carried; the gate counters "
             "show %s, %s and %s." % (c(f["loss_50"]), c(f["loss_30"]), c(f["loss_20"]), c(f["gate_50"]),
                                      c(f["gate_30"]), c(f["gate_20"])))
    L.append("3. Each Maplestead line holds a keg on tap and its weekly cover whatever it sells, read off the reps' "
             "summer counts at customers' own rates: %s fifty-litre and %s thirty-litre kegs, where the fleet's turns "
             "give their volume about %s thirty-litre kegs with the kegs on the way."
             % (c(f["estate_50"]), c(f["estate_30"]), c(r10(G["turns_estate"][30]))))
    L.append("4. The 2027 Foundry range racks 200-keg lots across up to 18 beers, so the cold store walked from the "
             "November stocktake through the brew plan holds %s full kegs in the 20 litre busiest week, against %s at "
             "the November days of cover." % (c(f["store"]), c(r10(h["store_cover"]["store"]))))
    L.append("5. The kegs needed in circulation are %s, %s and %s in the weeks ending %s, %s and %s: the existing "
             "trade's circulation rebuilt for 2026 from the stocktake, the washer and the fills and carried on its "
             "deliveries (circulation rises about %s, %s and %s per cent for each 1 per cent more delivered), plus the "
             "new lines, the cold store and the float.\n"
             % (c(f["need_50"]), c(f["need_30"]), c(f["need_20"]), f["week_50"], f["week_30"], f["week_20"],
                f["elasticity_50"], f["elasticity_30"], f["elasticity_20"]))
    L.append("# Step-by-Step\n")
    steps = [
        "Assemble the records: the depot gate counts (sizes written 50, 50L and K50; outages keyed the next day), "
        "the washer log by shift, the filling log, the repair jobs, the RFID reads (duplicate reads seconds apart "
        "dropped, replaced tags mapped back to their serials) and the delivery visits (handheld re-syncs dropped).",
        "Loss: the kegs filled in the year (%s, %s and %s) less the own kegs back at the washer (washed, sent to "
        "repair or condemned there, less repaired kegs presented again: %s, %s and %s), less the rise in kegs out "
        "between the two stocktakes from the tagged trips (%s to %s, %s to %s and %s to %s, scaled by the tagged "
        "share of fills), gives %s, %s and %s. The hurried route reads the gate counters and files %s, %s and %s: "
        "its in-and-out reconciliation closes because other brewers' kegs fill the gap."
        % (c(f["sent_50"]), c(f["sent_30"]), c(f["sent_20"]), c(f["back_50"]), c(f["back_30"]), c(f["back_20"]),
           c(f["out1_50"]), c(f["out2_50"]), c(f["out1_30"]), c(f["out2_30"]), c(f["out1_20"]), c(f["out2_20"]),
           c(f["loss_50"]), c(f["loss_30"]), c(f["loss_20"]), c(f["gate_50"]), c(f["gate_30"]), c(f["gate_20"])),
        "Fleet: the 2026 stocktake's clean empties and repair cage plus the tagged kegs out at 30 November that will "
        "come back (open trips completed from the same weeks of 2025, seasonal customers on their own), scaled to "
        "every keg, gives %s, %s and %s. The hurried route takes the register's active kegs."
        % (c(f["fleet_50"]), c(f["fleet_30"]), c(f["fleet_20"])),
        "Busiest week's deliveries: weekly deliveries on the calendar, warmth over 17 C, bank holidays, Christmas, "
        "January and trend, carried through 2027 at normal weather with the Maplestead pubs and the new Foundry taps "
        "from their start weeks: %s, %s and %s; replaying the 2016 to 2025 summers gives the 80 per cent ranges."
        % (c(f["deliv_50"]), c(f["deliv_30"]), c(f["deliv_20"])),
        "Maplestead: a customer's kegs of a size fitted on its taps and its order cover (its own year's rate over its "
        "delivery interval and a week) across the reps' summer counts; each pub's line at its scheduled rate holds "
        "%s fifty-litre and %s thirty-litre kegs in all. The hurried route carries their volume at the fleet's days "
        "out per trip." % (c(f["estate_50"]), c(f["estate_30"])),
        "Foundry: the cold store from the November stocktake, plus the brew plan's racking, less the range's forecast "
        "deliveries and the depots' stock beer by beer on sale, peaks at %s in the week ending %s. The hurried route "
        "carries the November days of cover." % (c(f["store"]), f["week_20"]),
        "Need: 2026 circulation rebuilt day by day (fleet from the 2025 stocktake run down by the loss, less clean "
        "empties from the washer and the fills), fitted on deliveries and carried to 2027; plus the new lines with "
        "their kegs filled and on the way back, the cold store and two days' season fills: %s, %s and %s."
        % (c(f["need_50"]), c(f["need_30"]), c(f["need_20"])),
        "Order: the need less the fleet in the busiest week (the fleet at 30 November less the year's loss per keg "
        "sent out carried to that week, %s, %s and %s): %s, %s and %s. The careful but hurried route (gate loss, "
        "register, the estate and the Foundry range at the fleet's turns) orders %s, %s and %s."
        % (c(f["lost_to_week_50"]), c(f["lost_to_week_30"]), c(f["lost_to_week_20"]), c(f["buy_50"]), c(f["buy_30"]),
           c(f["buy_20"]), c(r10(car["buy"][50])), c(r10(car["buy"][30])), c(r10(car["buy"][20]))),
        "No other conclusion survives: every rival method lands the order inside its band for each size, the "
        "register alone leaves 50 litre unordered, the turns alone under-order the 30 litre and 20 litre kegs, and the "
        "fleet's whole-pool turns over-order 50 litre kegs by about %s." % c(r10(h["fleet_turns"]["buy"][50] - f["buy_50"])),
    ]
    for i, t in enumerate(steps):
        L.append("%d. %s" % (i + 1, t))
    return "\n".join(L) + "\n"
