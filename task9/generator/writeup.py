"""task9: submission.md, the four answer blocks, written from the figures as computed (F) and as stated (F["stated"]).
Every number the blocks state goes through a helper that records it in STATED, which figures.json carries for
figures_check.py."""
import golden as GD

STATED = []


def _say(*xs):
    STATED.extend(str(x) for x in xs)


def n(v):
    s = "{:,}".format(int(round(v)))
    _say(s)
    return s


def usd(v):
    return "USD " + n(v)


def pct(v, k=0):
    s = ("%." + str(k) + "f") % (100 * v)
    _say(s)
    return s + " per cent"


def dec(v, k=2):
    s = ("%." + str(k) + "f") % v
    _say(s)
    return s


def build(F):
    del STATED[:]
    _say("2,000", "2,800", "1,000")      # the spec's intervals and the climb's unit, as the prompt states them
    S, B, G, R = F["stated"], F["bands"], F["gold"], F["routes"]
    A = F["A"]
    lo, hi = A.pairs["low"], A.pairs["high"]
    c, dose, sh, L1, ft = S["REC_counts"], S["R4_dose"], S["R2_shares"], S["R1_loss"], S["R3_ft_units"]
    lot = F["fwd_lot"]
    rc = lambda k, u: n(round(R[k][u], -1))
    L = []
    a = L.append

    a("## Tags")
    a("")
    a("**Domain:** Machine Learning Research, General Statistics & Data Science (Interpretability: feature attribution, "
      "probing, mechanistic analysis).")
    a("**Analytical objective:** Root-Cause Analysis.")
    a("")

    # ---- 1. Final Recommendation
    a("## Final Recommendation")
    a("")
    a("Take the conditioner disk out of the full PM under Rev G and change it after %s wafers of its own use on %s and %s and "
      "after %s on %s and %s, which saves about %s a year against Rev F as it stands: the disk's own wear carries %s of the edge "
      "ring's loss at sort (%s points of mean wafer sort yield from April to August) and cost %s more units at final test, and "
      "the disks every unit runs now (lot %s) start the ring at %s and %s wafers. Rejected: counts set on every disk lot's curve "
      "(%s and %s wafers), counts that leave final test out (%s and %s) or take it in proportion to the sort loss (%s and %s), "
      "and any change to the pad or the retaining ring." % (
          n(c[lo[0]]), lo[0], lo[1], n(c[hi[0]]), hi[0], hi[1], usd(S["R5_saving"]), pct(sh["disk"], 1), dec(L1["points"]),
          n(S["R3_total"]), lot, n(dose["%s onset" % lo[0]]), n(dose["%s onset" % hi[0]]), rc("REC_pooled", lo[0]),
          rc("REC_pooled", hi[0]), rc("REC_sort_only", lo[0]), rc("REC_sort_only", hi[0]), rc("REC_proportional", lo[0]),
          rc("REC_proportional", hi[0])))
    a("")

    # ---- 2. Supplementary Questions
    a("## Supplementary Questions")
    a("")
    a("### %s" % GD.DECK)
    a("")
    a("1. The loss at sort on wafers sorted 1 April to 31 August 2026: %s points of mean wafer sort yield (band %s to %s), each "
      "wafer's outermost-zone fails above its own interior fail rate plus the zone's fallout on disks short of their onset, over "
      "all %s sorted wafers with a retest replacing its first pass. The deck opens on it and charts the loss by sort month "
      "(January to March already at %s points)." % (dec(L1["points"]), dec(B["R1_loss"]["points"][0]), dec(B["R1_loss"]["points"][1]),
                                                    n(F["n_window"]), dec(G["R1_q1"])))
    a("2. Good die lost at sort by product, in a table beside that chart: P-A %s (band %s to %s), P-B %s (%s to %s), P-C %s (%s "
      "to %s), about %s at the cost inputs' die values." % tuple(
          sum([[n(L1["%s die" % p]), n(B["R1_loss"]["%s die" % p][0]), n(B["R1_loss"]["%s die" % p][1])] for p in ("P-A", "P-B", "P-C")], [])
          + [usd(S["R1_usd"])]))
    a("3. The parts and tools behind the loss at sort ranked by their share of it, in a table of the candidates the records "
      "carry: the conditioner disk's wear %s (band %s to %s), the pad's life on top of it %s (%s to %s), and the retaining ring's "
      "wear, deposition chamber DEP-3, scanner SC-4 at M1 and the deposition chambers' RF hours at none, each under %s (a fitted "
      "share below zero is none), with the evidence that rules each out (the six ring-only swaps, DEP-3's routing to %s and %s, "
      "SC-4's first lots at M1 on %s, %s days after Rev F took effect)." % (
          pct(sh["disk"], 1), pct(B["R2_shares"]["disk"][0]), pct(B["R2_shares"]["disk"][1]), pct(sh["pad"], 1),
          pct(B["R2_shares"]["pad"][0]), pct(B["R2_shares"]["pad"][1]), pct(B["R2_shares"]["ring"][1]), hi[0], hi[1],
          F["sc4_first"], n(F["sc4_after_rev_f"])))
    a("4. The units final test lost to the ring on the lots it finished 1 April to 31 August, by product, in a table beside a "
      "chart of burn-in failures by month: P-A %s (band %s to %s), P-B %s (%s to %s), P-C %s (%s to %s), %s in all, about %s at "
      "die value plus assembly and test. Each lot's burn-in failures above its units' base rate of %s per cent come from its "
      "wafers' outer-zone good die, rising with the disk's wear from about %s wafers of use on %s and %s and %s on %s and %s." % tuple(
          sum([[n(ft[p]), n(B["R3_ft_units"][p][0]), n(B["R3_ft_units"][p][1])] for p in ("P-A", "P-B", "P-C")], [])
          + [n(S["R3_total"]), usd(S["R3_usd"]), dec(S["ft_base"]), n(S["ft_start"][lo[0]]), lo[0], lo[1], n(S["ft_start"][hi[0]]),
             hi[0], hi[1]]))
    rows = []
    for u in lo + hi:
        rows.append("%s %s wafers (band %s to %s) and %s points per 1,000 wafers (%s to %s)" % (
            u, n(dose["%s onset" % u]), n(B["R4_dose"]["%s onset" % u][0]), n(B["R4_dose"]["%s onset" % u][1]),
            dec(dose["%s climb" % u], 1), dec(B["R4_dose"]["%s climb" % u][0], 1), dec(B["R4_dose"]["%s climb" % u][1], 1)))
    a("5. Each unit's usage at which the loss at sort starts, in wafers of the disk's own use, and the climb after it in points of "
      "the outermost sort zone's fail rate per 1,000 wafers, on the disks the units will be fitted with from September (lot %s: "
      "every unit runs it now, the earlier lots' last serials are fitted, and no disk has been received since): %s; charted as "
      "the zone's excess against disk use for each downforce pair, this lot beside the earlier ones. The bands' floors reach a "
      "unit's own fit on its one short disk of the lot and a fit that carries the lot's effect as one multiplier on every "
      "unit." % (lot, "; ".join(rows)))
    a("6. Each unit's change count for the disk once Rev G takes it out of the full PM, the ring costed at sort and at final test, "
      "in a table: %s and %s %s wafers (band %s to %s), %s and %s %s (%s to %s); a unit's own count inside these bands is "
      "accepted." % (lo[0], lo[1], n(c[lo[0]]), n(B["REC_counts"][lo[0]][0]), n(B["REC_counts"][lo[0]][1]),
                     hi[0], hi[1], n(c[hi[0]]), n(B["REC_counts"][hi[0]][0]), n(B["REC_counts"][hi[0]][1])))
    a("7. The yearly saving against Rev F as it stands: %s (band %s to %s), %s on %s and %s (%s to %s) and %s on %s and %s "
      "(%s to %s), at the FY27 plan's wafers per unit and product mix in the cost inputs, beside each unit's cost per wafer "
      "under both specs." % (
          usd(S["R5_saving"]), usd(B["R5_saving"][0]), usd(B["R5_saving"][1]), usd(S["R5_pair"]["low"]), lo[0], lo[1],
          usd(B["R5_pair"]["low"][0]), usd(B["R5_pair"]["low"][1]), usd(S["R5_pair"]["high"]), hi[0], hi[1],
          usd(B["R5_pair"]["high"][0]), usd(B["R5_pair"]["high"][1])))
    a("")

    # ---- 3. Critical Components
    a("## Critical Components")
    a("")
    a("1. The ring's loss at sort, %s points of mean wafer sort yield from April to August, measured on every wafer against the "
      "fallout a disk short of its onset leaves, not against the band's level before April (about %s points) or on the "
      "classifier's EDGE_RING wafers alone, which carry %s of it." % (dec(L1["points"]), dec(R["R1_q1_baseline"], 1),
                                                                     pct(1 - G["unflagged_share"])))
    a("2. The cause: the conditioner disk's own wear, %s of that loss with the pad's life adding %s on top of it; the retaining "
      "ring, DEP-3, SC-4 and the RF hours carry none." % (pct(sh["disk"], 1), pct(sh["pad"], 1)))
    a("3. The curve the count rests on is lot %s's, the disks every unit runs now: the loss starts at %s wafers on %s and %s and climbs %s "
      "points per 1,000 wafers, and at %s and %s on %s and %s; every lot fitted together puts the onsets at %s and %s." % (
          lot, n(dose["%s onset" % lo[0]]), lo[0], lo[1], dec(dose["%s climb" % lo[0]], 1), n(dose["%s onset" % hi[0]]),
          dec(dose["%s climb" % hi[0]], 1), hi[0], hi[1], n(round(R["R4_pooled"][lo[0]][0], -1)), n(round(R["R4_pooled"][hi[0]][0], -1))))
    a("")

    # ---- 4. Step-by-Step
    a("## Step-by-Step")
    a("")
    a("1. Clean the records: the latest sort record per wafer, product aliases mapped, the MES's wafer-level chamber steps "
      "joined to the units' polish record, each part's use counted from its own last replacement in the maintenance log's parts "
      "text (the EW-118 PMs keep the disk, the unscheduled swaps change one part), blank counters placed on the unit's polish "
      "record, and each disk's supplier lot read from the serial its entry fitted against the stores receipts' serial ranges.")
    a("2. Measure the ring at sort on every wafer as the outermost zone's fails above its interior rate plus the zone's fallout "
      "on disks short of their onset: %s points. The classifier's EDGE_RING wafers carry only %s of it, and the band's level "
      "before April as the baseline gives about %s points, because the ring already cost %s points from January to March." % (
          dec(L1["points"]), pct(1 - G["unflagged_share"]), dec(R["R1_q1_baseline"], 1), dec(G["R1_q1"])))
    a("3. Attribute that loss with one model per downforce pair and disk lot, the retaining ring, DEP-3, SC-4 and the RF hours "
      "beside the disk's hinge: the disk %s, the pad %s, the rest none. Tool commonality points at %s, which is routing and "
      "timing." % (pct(sh["disk"], 1), pct(sh["pad"], 1), ", ".join(x.split()[-1] for x in R["R2_commonality_top"][:-1]) + " and " +
                   R["R2_commonality_top"][-1].split()[-1]))
    a("4. Fit the outermost zone's excess on a hinge in the disk's own use, the pad's life on the slope, one fit per downforce "
      "pair and disk lot. Lot %s starts the ring at %s and %s wafers against %s and %s for the earlier lots, and it is the lot "
      "every unit runs now, the earlier lots' last serials fitted and no disk received since; one fit per pair over every disk "
      "gives %s and %s, and one fit for the fleet %s." % (lot, n(dose["%s onset" % lo[0]]), n(dose["%s onset" % hi[0]]), n(F["old_onsets"]["low"]),
                         n(F["old_onsets"]["high"]), n(round(R["R4_pooled"][lo[0]][0], -1)), n(round(R["R4_pooled"][hi[0]][0], -1)),
                         n(round(R["R4_fleet"][lo[0]][0], -1))))
    a("5. Model final test's burn-in failures lot by lot, sub-lots added back: a base rate on the lot's units plus a share of "
      "its wafers' outer-zone good die that rises with each disk's wear, measured as a share of its lot's onset, and levels "
      "off at %s per cent: %s units lost on the lots finished April to August. Burn-in taken in proportion to the ring's die at "
      "sort gives %s, because the damage starts before the ring shows; a base from the lots with no ring label gives %s." % (
          dec(S["ft_level"], 1), n(S["R3_total"]), n(round(sum(R["R3_proportional"].values()), -2)),
          n(round(sum(R["R3_clean_lot_base"].values()), -2))))
    a("6. Set each pair's count where the disk's cost per wafer (its %s change, the good die the ring takes at sort and the units "
      "final test scraps at the plan's mix) is lowest on lot %s's curve: %s and %s wafers. Left at the sort loss alone the counts "
      "are %s and %s; with final test in proportion to the sort loss, %s and %s; on every lot's curve, %s and %s." % (
          usd(A.allin["disk_change"]), lot, n(c[lo[0]]), n(c[hi[0]]), rc("REC_sort_only", lo[0]), rc("REC_sort_only", hi[0]),
          rc("REC_proportional", lo[0]), rc("REC_proportional", hi[0]), rc("REC_pooled", lo[0]), rc("REC_pooled", hi[0])))
    a("7. Price the saving against Rev F's own 2,800-wafer cycle on the same disks: %s a year. On every lot's curve it reads about "
      "%s, and with the summer's own loss rate taken as Rev F's about %s." % (
          usd(S["R5_saving"]), usd(round(R["R5_pooled"], -3)), usd(round(R["R5_summer_rate"], -3))))
    a("")
    a("No other conclusion survives: every sound reading of the fallout, the pairs, the weights and final test's rise keeps the "
      "loss at sort between %s and %s points, final test's units within 12 per cent, the counts inside 8 per cent and the saving "
      "between %s and %s, while each shortcut lands outside: the classifier and the pre-April baseline under-measure the loss, "
      "burn-in in proportion to the sort loss misses most of final test's, and pooling the disk lots or leaving final test out "
      "of the count puts the counts %d per cent or more too long." % (
          dec(B["R1_loss"]["points"][0]), dec(B["R1_loss"]["points"][1]), usd(B["R5_saving"][0]), usd(B["R5_saving"][1]),
          F["shortcut_range"][0]))
    _say("8", "12", str(F["shortcut_range"][0]))
    a("")
    return "\n".join(L)
