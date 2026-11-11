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
    c, dose, br, sh = S["R6_counts"], S["R4_dose"], S["R5_bridge"], S["R3_shares"]
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
    a("Take the conditioner disk out of the full PM under Rev G and change it after %s wafers of its own use on %s and %s "
      "and after %s on %s and %s, which saves about %s a year against Rev F as it stands: the disk's own wear carries %s of the "
      "edge ring's loss of %s points of mean sort yield since April, and the high-downforce pair's disks reach the ring's "
      "onset at %s wafers against %s. Rejected: one count for all four units (about %s wafers, about %s a year worse), a "
      "return to Rev E (about %s a year worse), and any change to the pad or the retaining ring, which carry none of the loss beyond the pad's "
      "%s on top of the disk's." % (
          n(c[lo[0]]), lo[0], lo[1], n(c[hi[0]]), hi[0], hi[1], usd(S["R7_saving"]), pct(sh["disk"], 1), dec(S["R1_points"]),
          n(dose["%s onset" % hi[0]]), n(dose["%s onset" % lo[0]]), n(round(R["R6_fleet"][lo[0]], -1)), usd(round(F["fleet_vs_g"], -3)),
          usd(round(F["rev_e_vs_g"], -3)), pct(sh["pad"], 1)))
    a("")

    # ---- 2. Supplementary Questions
    a("## Supplementary Questions")
    a("")
    a("### %s" % GD.DECK)
    a("")
    a("1. The loss on wafers sorted 1 April to 31 August 2026: %s points of mean wafer sort yield (band %s to %s), each "
      "wafer's outermost-zone fails above its own interior fail rate plus the zone's fallout at a fresh disk, over all %s "
      "sorted wafers with a retest replacing its first pass. The deck opens on it and charts the loss by sort month (January "
      "to March already at %s points)." % (dec(S["R1_points"]), dec(B["R1_points"][0]), dec(B["R1_points"][1]), n(F["n_window"]),
                                           dec(G["R1_q1"])))
    a("2. Good die lost by product, in a table beside that chart: P-A %s (band %s to %s), P-B %s (%s to %s), P-C %s (%s to %s), "
      "about %s at the cost inputs' die values." % (
          n(S["R2_die"]["P-A"]), n(B["R2_die"]["P-A"][0]), n(B["R2_die"]["P-A"][1]), n(S["R2_die"]["P-B"]), n(B["R2_die"]["P-B"][0]),
          n(B["R2_die"]["P-B"][1]), n(S["R2_die"]["P-C"]), n(B["R2_die"]["P-C"][0]), n(B["R2_die"]["P-C"][1]), usd(S["R2_usd"])))
    a("3. The causes ranked by their share of that loss, in a table: the conditioner disk's wear %s (band %s to %s), the pad's "
      "life on top of it %s (%s to %s), and the retaining ring (%s), DEP-3 (%s), SC-4 (%s) and the deposition chambers' RF "
      "hours (%s) at none, each within %s of zero, with the evidence that rules each out (the six ring-only swaps, DEP-3's "
      "routing to %s and %s, SC-4's start a week after Rev F)." % (
          pct(sh["disk"], 1), pct(B["R3_shares"]["disk"][0]), pct(B["R3_shares"]["disk"][1]), pct(sh["pad"], 1),
          pct(B["R3_shares"]["pad"][0]), pct(B["R3_shares"]["pad"][1]), pct(sh["ring"], 1), pct(sh["dep3"], 1), pct(sh["sc4"], 1),
          pct(sh["rf"], 1), pct(B["R3_shares"]["ring"][1], 1), hi[0], hi[1]))
    rows = []
    for u in lo + hi:
        rows.append("%s %s wafers (band %s to %s) and %s points per 1,000 wafers (%s to %s)" % (
            u, n(dose["%s onset" % u]), n(B["R4_dose"]["%s onset" % u][0]), n(B["R4_dose"]["%s onset" % u][1]),
            dec(dose["%s slope" % u], 1), dec(B["R4_dose"]["%s slope" % u][0], 1), dec(B["R4_dose"]["%s slope" % u][1], 1)))
    a("4. Each unit's usage at which the loss starts, in wafers of the disk's own use, and the climb after it in points of "
      "the outermost sort zone's fail rate per 1,000 wafers: %s; charted as the zone's excess against disk use for each "
      "downforce pair." % "; ".join(rows))
    a("5. The shares of the loss, as a bar chart: %s that the 2,000-wafer rule would have cost anyway (band %s to %s), %s that "
      "Rev F's move to 2,800 added (%s to %s) and %s that the EW-118 waiver's retained disks added (%s to %s), each rule run "
      "on each unit's own polish sequence." % (
          pct(br["old_rule"]), pct(B["R5_bridge"]["old_rule"][0]), pct(B["R5_bridge"]["old_rule"][1]), pct(br["rev_f"]),
          pct(B["R5_bridge"]["rev_f"][0]), pct(B["R5_bridge"]["rev_f"][1]), pct(br["ew118"]), pct(B["R5_bridge"]["ew118"][0]),
          pct(B["R5_bridge"]["ew118"][1])))
    a("6. Each unit's change count for the disk once Rev G takes it out of the full PM, in a table: %s and %s %s wafers (band "
      "%s to %s), %s and %s %s (%s to %s)." % (lo[0], lo[1], n(c[lo[0]]), n(B["R6_counts"][lo[0]][0]), n(B["R6_counts"][lo[0]][1]),
                                              hi[0], hi[1], n(c[hi[0]]), n(B["R6_counts"][hi[0]][0]), n(B["R6_counts"][hi[0]][1])))
    a("7. The yearly saving against Rev F as it stands: %s (band %s to %s), %s on %s and %s and %s on %s and %s, at %s wafers "
      "a year split by each unit's share since 1 June, beside each unit's cost per wafer under both specs." % (
          usd(S["R7_saving"]), usd(B["R7_saving"][0]), usd(B["R7_saving"][1]), usd(round(G["R7_unit"][lo[0]] + G["R7_unit"][lo[1]], -3)),
          lo[0], lo[1], usd(round(G["R7_unit"][hi[0]] + G["R7_unit"][hi[1]], -3)), hi[0], hi[1], n(F["wpy"])))
    a("")

    # ---- 3. Critical Components
    a("## Critical Components")
    a("")
    a("1. The ring's loss, %s points of mean wafer sort yield from April to August, measured on every wafer against the "
      "fallout a fresh disk leaves, not against the band's level before April (%s)." % (dec(S["R1_points"]), dec(R["R1_q1_baseline"])))
    a("2. The dose on the disk's own use, by downforce pair: the loss starts at %s wafers on %s and %s and climbs %s points per "
      "1,000 wafers, and at %s and %s on %s and %s." % (
          n(dose["%s onset" % lo[0]]), lo[0], lo[1], dec(dose["%s slope" % lo[0]], 1), n(dose["%s onset" % hi[0]]),
          dec(dose["%s slope" % hi[0]], 1), hi[0], hi[1]))
    a("3. The rules' shares, each rule run on each unit's own wafers: %s the 2,000-wafer rule's own exposure, %s Rev F's "
      "extension, %s the EW-118 retained disks." % (pct(br["old_rule"]), pct(br["rev_f"]), pct(br["ew118"])))
    a("")

    # ---- 4. Step-by-Step
    a("## Step-by-Step")
    a("")
    a("1. Clean the records: the latest sort record per wafer, product aliases mapped, the MES's wafer-level chamber steps "
      "joined to the units' polish record, and each part's use counted from its own last replacement in the maintenance "
      "log's parts text (the EW-118 PMs keep the disk, the unscheduled swaps change one part), blank counters placed on the "
      "unit's polish record.")
    a("2. Measure the ring on every wafer as the outermost zone's fails above its interior rate plus the zone's fallout on "
      "disks short of their onset: %s points. The classifier's EDGE_RING wafers alone give %s, and the band's level before "
      "April as the baseline gives %s, because the ring already cost %s points from January to March." % (
          dec(S["R1_points"]), dec(R["R1_labels"]), dec(R["R1_q1_baseline"]), dec(G["R1_q1"])))
    a("3. Fit the outermost zone's excess on a hinge in the disk's own use, with the pad's life on the slope, one fit per "
      "downforce pair: onsets %s and %s wafers. One fit over the fleet gives %s for every unit; wafers since the full PM put "
      "the onsets at %s and %s." % (n(dose["%s onset" % lo[0]]), n(dose["%s onset" % hi[0]]), n(R["R4_fleet"][lo[0]][0]),
                                    n(R["R4_since_full"][lo[0]][0]), n(R["R4_since_full"][hi[0]][0])))
    a("4. Attribute the loss with each disk life's own slope beside the retaining ring, DEP-3, SC-4 and the RF hours: the disk "
      "%s, the pad %s, the rest none. Read wafer by wafer, the joint fit gives the retaining ring %s, which the six ring-only "
      "swaps refute; tool commonality points at %s and %s and DEP-3, which is routing." % (
          pct(sh["disk"], 1), pct(sh["pad"], 1), pct(R["R3_joint"]["ring"], 1), hi[0], hi[1]))
    a("5. Run the 2,000-wafer rule, Rev F and the actual history on each unit's own polish sequence and read the ring off the "
      "pair's curve: %s, %s and %s. Slicing the observed loss at 2,000 and 2,800 wafers of disk use gives %s, %s and %s." % (
          pct(br["old_rule"]), pct(br["rev_f"]), pct(br["ew118"]), pct(R["R5_slice"]["old_rule"]), pct(R["R5_slice"]["rev_f"]),
          pct(R["R5_slice"]["ew118"])))
    a("6. Set each pair's count where the disk's cost per wafer (its %s change and the good die the ring takes at the "
      "summer's mix) is lowest: %s and %s wafers. A dose from zero gives %s and %s; moving the full PM instead gives %s and %s." % (
          usd(A.allin["disk_change"]), n(c[lo[0]]), n(c[hi[0]]), n(round(R["R6_linear"][lo[0]], -1)), n(round(R["R6_linear"][hi[0]], -1)),
          n(round(R["R6_full_pm_lever"][lo[0]], -1)), n(round(R["R6_full_pm_lever"][hi[0]], -1))))
    a("7. Price the saving against Rev F's own 2,800-wafer cycle with the waiver ended: %s a year. The summer's own loss rate "
      "taken as Rev F's gives about %s, because it carries the retained disks." % (usd(S["R7_saving"]), usd(round(R["R7_summer_rate"], -3))))
    a("")
    a("No other conclusion survives: every sound reading of the fallout, the pairs, the weights and the mix keeps the loss "
      "between %s and %s points, the counts inside 8 per cent and the saving between %s and %s, while each shortcut lands "
      "outside: the classifier and the pre-April baseline under-measure the loss, the wafer-level fit gives the retaining "
      "ring a share its swaps deny, slicing mis-splits the rules, and the summer's rate nearly triples the saving." % (
          dec(B["R1_points"][0]), dec(B["R1_points"][1]), usd(B["R7_saving"][0]), usd(B["R7_saving"][1])))
    _say("8")
    a("")
    return "\n".join(L)
