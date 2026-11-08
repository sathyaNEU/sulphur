"""figures.json and submission.md, both from the figures analysis.py computed on the pack (never typed)."""
import math

import analysis as A
import golden as GD


def r100(x):
    return int(100 * math.floor(x / 100.0 + 0.5))


def r10(x):
    return int(10 * math.floor(x / 10.0 + 0.5))


def fmt(n):
    return "{:,}".format(int(n))


def rungs(pk, res):
    offer = A.offered(pk)
    tid = A.time_in_district(pk)
    d_set = [c for c in offer if tid[c][1] > tid[c][2]]
    d_net = sum(tid[c][1] - tid[c][2] for c in d_set)
    r1 = A.removal_one(pk, res)
    o_set = [c for c in offer if r1[c][2] > 0]
    o_net = sum(r1[c][2] for c in o_set)
    prop = A.proportional_carry(pk, res)
    return {"default_set": d_set, "default_net": d_net, "default_net_rounded": GD.r5000(d_net),
            "tid": tid, "one_set": o_set, "one_net": o_net, "one_net_rounded": GD.r5000(o_net),
            "prop_net": prop, "prop_net_rounded": GD.r5000(prop)}


def pieces(pk, res):
    t5 = res["runs"]["R05"]["table"]
    t4 = res["runs"]["R04"]["table"]
    t7 = res["runs"]["R07"]["table"]
    return {
        "lee_let_h": r10(t5[("LEE", "LET")][0]), "lee_let_cost": r100(t5[("LEE", "LET")][0] * pk.rate),
        "lee_let_charge": r100(t5[("LEE", "LET")][1]),
        "lee_let_lo": int(500 * math.floor(t5[("LEE", "LET")][0] * pk.rate / 500.0)),
        "lee_let_hi": int(500 * math.ceil(t5[("LEE", "LET")][0] * 1.15 * pk.rate / 500.0)),
        "lee_let_even": r10(t5[("LEE", "LET")][1] / pk.rate),
        "corridor_cost": r100(t5[("LEE", "LET", "CLI")][0] * pk.rate), "corridor_charge": r100(t5[("LEE", "LET", "CLI")][1]),
        "ban_alone_h": r10(t7[("BAN",)][0]), "ban_alone_cost": r100(t7[("BAN",)][0] * pk.rate),
        "ban_charge": r100(t7[("BAN",)][1]),
        "erris_h": GD.r100(t7[("BAN", "BLM")][0]), "blm_alone_h": r10(t7[("BLM",)][0]),
        "mul_alone_h": r10(t4[("MUL",)][0]), "mul_alone_cost": r100(t4[("MUL",)][0] * pk.rate),
        "mul_charge": r100(t4[("MUL",)][1]), "achill_h": GD.r100(t4[("MUL", "ACH")][0]),
        "ach_alone_h": r10(t4[("ACH",)][0]),
        "mul_marg_cost": r100((t4[("MUL", "ACH")][0] - t4[("ACH",)][0]) * pk.rate),
        "ban_marg_cost": r100((t7[("BAN", "BLM")][0] - t7[("BLM",)][0]) * pk.rate),
    }


def figures(pk, res, fig):
    rg = rungs(pk, res)
    pc = pieces(pk, res)
    tid = rg["tid"]
    return {
        "call_set": fig["set"], "net_saving_rounded": fig["net_saving_rounded"], "net_saving_exact": round(fig["net_saving"]),
        "price": fig["price"], "rate": fig["rate"],
        "runs_saved_h": {r: d["saved_h_rounded"] for r, d in fig["runs"].items()},
        "runs_before_h": {r: d["before_rounded"] for r, d in fig["runs"].items()},
        "runs_after_h": {r: d["after_rounded"] for r, d in fig["runs"].items()},
        "pieces": pc,
        "default_set": rg["default_set"], "default_net_rounded": rg["default_net_rounded"],
        "default_lee_cost": r100(tid["LEE"][1]), "default_let_cost": r100(tid["LET"][1]),
        "default_lee_charge": r100(tid["LEE"][2]), "default_let_charge": r100(tid["LET"][2]),
        "one_set": rg["one_set"], "one_net_rounded": rg["one_net_rounded"],
        "prop_net_rounded": rg["prop_net_rounded"],
        "districts_parcels": {c: d["parcels_2027"] for c, d in fig["districts"].items()},
        "years": [2025, 2026, 2027], "standard_sections": ["4.1", "4.3", "3.2", "2.3"], "rounding": [50, 5000],
    }


def write(path, pk, res, fig):
    rg = rungs(pk, res)
    pc = pieces(pk, res)
    tid = rg["tid"]
    name = lambda c: pk.reg[c]["name"]
    gone = [name(c) for c in fig["set"]]
    stay = [name(c) for c in A.offered(pk) if c not in fig["set"]]
    lst = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1]
    R = fig["runs"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Other, Urban & Regional Science (supply chain and logistics: last-mile route economics of a "
               "retailer's own van fleet).  ")
    out.append("**Task type:** forecasting (demand, load and capacity prediction).  ")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## Final Recommendation\n")
    out.append("**Hand %s to Owenduff from January 2027 and keep %s: the hand-over saves about EUR %s net in 2027.** "
               "Pricing each district at the van time its own stops take hands Leenane and Letterfrack over too and "
               "claims EUR %s, but the Connemara van drives through both on its way to Clifden, which stays, so they "
               "save only their own stops; and pricing districts one at a time keeps Mulranny and Bangor Erris, which "
               "become the end of the Achill and Erris runs once Achill and Belmullet go.\n"
               % (lst(gone), lst(stay), fmt(fig["net_saving_rounded"]), fmt(rg["default_net_rounded"])))
    out.append("## Supplementary Questions\n")
    out.append("### %s\n" % GD.XLSX)
    out.append("1. A Districts sheet with one row per district in Owenduff's offer, in the offer's order, giving the "
               "code, the district, its run, its 2027 plan parcels, Owenduff's 2027 charge and the decision: %s go; "
               "%s stay." % (lst(gone), lst(stay)))
    rl = "; ".join("%s %s %s" % (r, d["name"], fmt(d["saved_h_rounded"])) for r, d in R.items())
    out.append("2. A Runs sheet with one row per run that serves an offered district, giving the districts it hands "
               "over, its 2027 van-hours as things stand and after the hand-over, and the van-hours saved, to the "
               "nearest hundred: %s." % rl)
    out.append("3. The sheet ends on the year's net saving after Owenduff's charges: EUR %s (to the nearest EUR 5,000)."
               % fmt(fig["net_saving_rounded"]))
    out.append("\n### %s\n" % GD.PNG)
    bl = "; ".join("%s %s" % (r, fmt(d["before_rounded"])) for r, d in R.items())
    out.append("4. Paired bars for each of those runs, 2027 van-hours as things stand beside 2027 after the hand-over "
               "(the hours as things stand less the hours saved), each bar labelled with its value to the nearest 50 "
               "(as things stand: %s), with the title stating the districts that go "
               "and the net saving of about EUR %s.\n" % (bl, fmt(fig["net_saving_rounded"])))
    out.append("## Critical Components\n")
    out.append("1. On the Connemara run, Leenane and Letterfrack together take only **about %s van-hours** off 2027 "
               "(EUR %s to %s at the van-hour rate, as the fit varies), far short of the **some %s van-hours** "
               "Owenduff's **EUR %s** for their parcels would pay for, because the van drives through both to "
               "reach Clifden; the whole run beyond Aghagower costs EUR %s against Owenduff's EUR %s, so the run keeps "
               "all three." % (fmt(pc["lee_let_h"]), fmt(pc["lee_let_lo"]), fmt(pc["lee_let_hi"]), fmt(pc["lee_let_even"]),
                               fmt(pc["lee_let_charge"]),
                               fmt(pc["corridor_cost"]), fmt(pc["corridor_charge"])))
    out.append("2. Bangor Erris on its own takes **%s van-hours** off the Erris run (EUR %s against Owenduff's EUR %s), "
               "but with Belmullet gone it is the end of the run, and the two together take **%s van-hours** off it."
               % (fmt(pc["ban_alone_h"]), fmt(pc["ban_alone_cost"]), fmt(pc["ban_charge"]), fmt(pc["erris_h"])))
    out.append("3. Mulranny on its own takes **%s van-hours** off the Achill run (EUR %s against Owenduff's EUR %s); "
               "with Achill gone, Mulranny and Achill together take **%s van-hours** off it."
               % (fmt(pc["mul_alone_h"]), fmt(pc["mul_alone_cost"]), fmt(pc["mul_charge"]), fmt(pc["achill_h"])))
    out.append("4. The 2027 van-hours are a forecast of road sections driven on the days a district beyond them has a "
               "stop, from the plan's stops month by month; carrying the last twelve months' hours forward in "
               "proportion to parcels overstates the year's net saving at **EUR %s**, against **EUR %s**.\n"
               % (fmt(rg["prop_net_rounded"]), fmt(fig["net_saving_rounded"])))
    out.append("## Step-by-Step\n")
    steps = [
        "Read Owenduff's offer (the offered districts, EUR %.2f a parcel delivered in 2027, any combination) and NPS-3 "
        "section 4 (the saving is the cost at the 2027 all-in rate of the van-hours the hand-over takes off the "
        "runs, less Owenduff's charges; the districts handed over are those whose hand-over lowers the year's cost "
        "most); took EUR %.2f a van-hour from the 2027 rate card and the delivery days from the 2027 calendar."
        % (fig["price"], fig["rate"]),
        "Cleaned the stop log: dropped the stop rows a handheld sent again when it re-synced (same stop and times, "
        "later sync), mapped CBN and CBS back to Castlebar town through the register's code changes, kept failed "
        "attempts and collections as stops, and timed each drive from the previous stop's departure, the break or "
        "depot out in the van run log.",
        "Read each run's road order from the stop sequences: every run sweeps its districts outward and drives back "
        "from the farthest one it served that day.",
        "The field's cost-to-serve build, each district's drive in from the stop before, the drives between its "
        "stops and its door time over November 2025 to October 2026 carried to 2027 by plan parcels, hands over %s "
        "and claims EUR %s; it prices Leenane at EUR %s and Letterfrack at EUR %s against Owenduff's EUR %s and EUR "
        "%s." % (lst([name(c) for c in rg["default_set"]]), fmt(rg["default_net_rounded"]), fmt(r100(tid["LEE"][1])),
                 fmt(r100(tid["LET"][1])), fmt(r100(tid["LEE"][2])), fmt(r100(tid["LET"][2]))),
        "That build charges a district with drive its run makes anyway: on the run-days when Leenane or Letterfrack had "
        "no stop the Connemara van still drove the road through them to Clifden, so their saving is the run time "
        "without their stops, not the time their stops take.",
        "Fitted each run's road sections and district access times by least squares on the observed drives between "
        "districts and to and from the depot (2025 and 2026), and each district's door time and drive between its "
        "own stops; the fit reproduces the drives on the run-days that skipped a district.",
        "Priced districts one at a time on that model: it hands over only %s (EUR %s), because Mulranny and Bangor "
        "Erris save little while Achill and Belmullet stay beyond them." % (lst([name(c) for c in rg["one_set"]]),
                                                                           fmt(rg["one_net_rounded"])),
        "Evaluated every combination of offered districts on each run, since handing over a district at the end makes "
        "the one before it the end: Mulranny with Achill and Bangor Erris with Belmullet take %s and %s van-hours "
        "off their runs, more than Owenduff charges, while no combination on the Connemara, Cong or East Mayo runs "
        "saves money." % (fmt(pc["achill_h"]), fmt(pc["erris_h"])),
        "Forecast 2027: each district's stops a delivery day month by month from the plan's parcels at its own stops "
        "a parcel, each road section driven with the probability that some district beyond it has a stop; the year's "
        "net saving is EUR %s, where carrying the last twelve months' hours in proportion to parcels gives EUR %s."
        % (fmt(fig["net_saving_rounded"]), fmt(rg["prop_net_rounded"])),
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("No other list survives: NPS-3 4.1 counts the van-hours a hand-over takes off the runs, so time in "
               "district (which counts the road through Leenane and Letterfrack the Connemara van still drives) and "
               "allocation by stops or parcels are out; NPS-3 4.3 asks for the districts whose hand-over together "
               "lowers the year's cost most, so one-at-a-time pricing is out on the Achill and Erris runs; the fit on "
               "2025 alone, on 2026 alone, with median drives, with annual rather than monthly stops, or a regression "
               "of run-day hours on the districts reached all give the same list and a net saving that rounds to "
               "EUR %s." % fmt(fig["net_saving_rounded"]))
    open(path, "w").write("\n".join(out) + "\n")
