"""task9: submission.md, the four answer blocks, every number from figures.json."""


def n(x):
    return "{:,}".format(x) if isinstance(x, int) else str(x)


def band(fg, key, cell=None):
    b = fg["bands"][key] if cell is None else fg["bands"][key][cell]
    return "%s to %s" % (n(b[0]), n(b[1]))


def build(fg):
    s, l, b, e, t = fg["R1_shortfall"], fg["R2_loop"], fg["R3_bath"], fg["R4_edge"], fg["R5_etch"]
    p, sh = fg["R7_plan"], fg["shortcut"]
    order = sorted([("R4", e, "DP2B's SH-300-C showerhead together with CM3's R8 zone 5 tune (thick edge on DP2B wafers "
                     "CM3 does not polish, thin edge on other chambers' wafers CM3 does)",
                     "fit SH-300-B to DP2B on 23 November, the day the plan takes CM3 back to its standard recipe (one cause, because the "
                     "two shifts cancel on the DP2B wafers CM3 polishes and neither change alone removes the loss); CM3's recipe "
                     "change alone recovers %s good die a VX40 wafer, not the %s its thin-edge fails suggest" % (fg["harmonise_alone_vx40"], fg["harmonise_claimed_vx40"])),
                    ("R2", l, "the oxide slurry loop SDS-OX1 since P-02A was slowed for energy on 2 June, scratching rising with "
                     "each polisher's distance along the loop", "return P-02A to its spring setpoint (filters and pads on CM1 and "
                     "CM3 change nothing)"),
                    ("R3", b, "the pre-gate bench tank T3 on the longer chemical life from 1 July, its metals "
                     "building with every lot between spikes and drain-and-fills", "the spike and drain-and-fill intervals "
                     "WB-1 and WB-2 ran before 1 July"),
                    ("R5", t, "CT-DEEP-07's polymer on ET1B and ET3A, building %s times faster per RF second than the "
                     "standard recipes" % fg["polymer_factor"], "wet-clean ET1B and ET3A every %s wafers at the Q1 mix "
                     "(%s), not at the fleet standard" % (n(t["interval"]), band(fg, "R5", "interval")))],
                   key=lambda x: -x[1]["VX40"])
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science, Interpretability (feature attribution and mechanistic analysis).  ")
    L.append("**Analytical objective:** Root-Cause Analysis.\n")
    L.append("## Final Recommendation\n")
    L.append("**Before VR90's first lots reach these steps, restore the oxide slurry loop's flow, put the pre-gate bench back "
             "on its spring chemical life, fit SH-300-B to DP2B on 23 November, the day the plan takes CM3 back to its standard "
             "recipe, and wet-clean ET1B and "
             "ET3A every %s wafers: VR90 then sorts at %s per cent in Q1 2027 and the commitment needs %s wafer starts, "
             "where the ramp plan as filed sorts it at %s per cent.** This rejects the polisher-by-polisher reading (filters "
             "and pads on CM1 and CM3, CM3's harmonisation as the edge fix, etch cleans on the wafer counter, VR90 read on "
             "a die-area formula), which puts VR90 at %s per cent under the plan and leaves the plan's losses in place.\n"
             % (n(t["interval"]), fg["R6_fixed"], n(p["starts"]), p["plan"], sh["careful_plan"]))
    L.append("## Supplementary Questions\n")
    L.append("### vr90_ramp_yield_review.xlsx\n")
    L.append("1. Sheet Shortfall, one row each for VX40 and VP12 with the mean good die per wafer sorted 1 January to 31 March "
             "2026, sorted 1 June to 30 September 2026 (final sort insertion of every wafer) and the shortfall: VX40 %s good "
             "die per wafer (%s), VP12 %s (%s)." % (s["VX40"], band(fg, "R1", "VX40"), s["VP12"], band(fg, "R1", "VP12")))
    items = []
    for k, (rid, c, what, fix) in enumerate(order):
        items.append("(%d) %s: %s good die per VX40 wafer (%s); fix: %s" % (k + 1, what, c["VX40"], band(fg, rid, "VX40"), fix))
    L.append("2. Sheet Causes, the causes ranked by good die per VX40 wafer sorted June to September, with the evidence, the "
             "fix and what that fix alone adds to VR90 under the plan: " + "; ".join(items) + ". The line's own variation "
             "leaves %s." % fg["residual_vx40"])
    L.append("3. Sheet VR90 Q1 2027: with every cause fixed VR90 sorts at %s per cent (%s); fixing each cause alone under the "
             "ramp plan as filed adds %s points for the slurry loop (%s), %s for the etch cleans (%s), %s for the chemical "
             "life (%s) and %s for SH-300-B on DP2B (%s); under the plan as filed VR90 sorts at %s per cent (%s); the Q1 "
             "commitment needs %s wafer starts with every cause fixed (%s)."
             % (fg["R6_fixed"], band(fg, "R6"), l["VR90"], band(fg, "R2", "VR90"), t["VR90"], band(fg, "R5", "VR90"),
                b["VR90"], band(fg, "R3", "VR90"), e["VR90"], band(fg, "R4", "VR90"), p["plan"], band(fg, "R7", "plan"),
                n(p["starts"]), band(fg, "R7", "starts")))
    L.append("4. Sheets Loop by polisher and Routes: bin 5 die per VX40 wafer by polisher, its distance along SDS-OX1 and the "
             "loop's state; and each shortcut's VR90 figures beside this review's.")
    L.append("\n### vr90_ramp_yield_note.docx\n")
    L.append("5. A note of about one page for the ramp review: the call and the two VR90 yields first, the four causes with "
             "the evidence that separates each from its rival, VR90's build-up, and the four changes as a numbered list.\n")
    L.append("## Critical Components\n")
    br, ar = fg["bin5_by_polisher"], fg["bin5_at_risk"]
    L.append("1. The scratch loss is the slurry loop's: bin 5 die per VX40 wafer, by polish time, rose from **%s** on wafers "
             "polished before 2 June to **%s** on wafers polished from 2 June with P-02A slowed (the standby fortnight "
             "aside) on CM3 (318 m along SDS-OX1; %s and %s counted on the die not already failed at bins 3 and 4) and from "
             "**%s** to **%s** on CM2 (64 m; %s and %s), and fell back on the standby pump; restoring the flow alone adds "
             "**%s** points to VR90 under the plan, which polishes on CM1 and CM3."
             % (br["CM3"]["spring"], br["CM3"]["slow"], ar["CM3"]["spring"], ar["CM3"]["slow"],
                br["CM2"]["spring"], br["CM2"]["slow"], ar["CM2"]["spring"], ar["CM2"]["slow"], l["VR90"]))
    L.append("2. DP2B's thick edge and CM3's thin-edge tune cancel on the DP2B wafers CM3 polishes (no excess there) and "
             "together cost **%s** good die per VX40 wafer; CM3's standard recipe alone recovers **%s**, not the %s its thin-edge fails suggest."
             % (e["VX40"], fg["harmonise_alone_vx40"], fg["harmonise_claimed_vx40"]))
    L.append("3. Contact-etch polymer builds **%s** times faster per RF second on CT-DEEP-07, so at VR90's planned share ET1B "
             "and ET3A must be cleaned every **%s** wafers; the fleet standard clean costs VR90 **%s** points."
             % (fg["polymer_factor"], n(t["interval"]), t["VR90"]))
    L.append("4. Read in blocks of die at VR90's own die area, January to March's clustered defects (cluster factor **%s**) give VR90 "
             "**%s** per cent with every cause fixed, where a Poisson die-area formula gives %s."
             % (fg["nb_alpha"], fg["R6_fixed"], sh["poisson_fixed"]))
    L.append("5. Under the ramp plan as filed VR90 sorts at **%s** per cent, and the commitment needs **%s** wafer starts with "
             "every cause fixed against %s under the plan." % (p["plan"], n(p["starts"]), n(fg["vr90_starts_plan"])))
    L.append("\n## Step-by-Step\n")
    st = [
        "Took each wafer's final insertion from `fab2_yield.sqlite` and compared mean good die per wafer sorted June to "
        "September with January to March: VX40 %s, VP12 %s." % (s["VX40"], s["VP12"]),
        "Joined bin 5 to each wafer's polisher and polish time (the four polishers' own exports, CM1's clock four minutes "
        "fast, CM3's in German locale) and the loop's state from `sds_ox1_trend_export.csv` (flow in L/min, then gpm): the "
        "excess grows with each tap's distance in `facility_line_list.xlsx` and vanishes on the standby pump, so it is the "
        "loop; booking the far taps' extra to CM1's and CM3's own consumables leaves VR90's loop gain at %s points, against %s."
        % (sh["uniform_loop_vr90"], l["VR90"]),
        "Rebuilt tank T3's metals lot by lot from `pgc_bench_controller.jsonl` (WB-2 in UTC, restart repeats dropped), with "
        "the drag per wafer (%s ppb) and the fresh level fitted to `lab_bath_metals_2026.xlsx`, and fitted bin 6 per die at "
        "risk against it scaled by gate oxide area: the July life costs VX40 %s; carried at the summer's own loading it adds "
        "%s points to VR90, but replayed at the plan's loading it adds %s."
        % (fg["bath_drag_ppb_per_wafer"], b["VX40"], sh["q3_bath_vr90"], b["VR90"]),
        "Classed every wafer by its deposition chamber (`ild0_dep_wafer_log.csv`) and polisher against the dates of the "
        "showerhead change and CM3's R8: DP2B wafers off CM3 fail bin 3 at the edge, other chambers' wafers on CM3 fail bin 4, "
        "DP2B wafers on CM3 fail neither, as `ild0_thickness_49pt.csv` shows (the 5-site SPC cannot); together %s good die per "
        "VX40 wafer, and CM3's standard recipe alone gains %s, not the %s its thin-edge fails suggest." % (e["VX40"], fg["harmonise_alone_vx40"], fg["harmonise_claimed_vx40"]),
        "Fitted the daily monitor adders on each chamber's load since its wet clean with CT-DEEP-07's polymer per RF second "
        "free: it builds %s times faster and flakes above %s RF seconds; scaled by RF time alone the clean would be %s "
        "wafers and VR90's loss %s points, against %s and %s."
        % (fg["polymer_factor"], n(fg["polymer_onset_rf_s"]), n(sh["kappa1_interval"]), sh["kappa1_vr90"], n(t["interval"]),
           t["VR90"]),
        "Read January to March's bin 8 in blocks of VX40 and VP12 die and fitted a negative binomial (cluster factor %s): "
        "VR90 keeps %s per cent of its die clear of random defects; a Poisson formula on VX40's die yield "
        "puts VR90 at %s per cent with every cause fixed, a cluster factor of 2 at %s." % (fg["nb_alpha"], fg["vr90_random_yield_pct"],
                                                                                         sh["poisson_fixed"], sh["alpha2_fixed"]),
        "Multiplied the mechanisms' survival on VR90's own die under the plan's conditions. With every cause fixed: random "
        "defects %s per cent, scratches %s (the spring flow's level on CM1 and CM3 in VR90-T's own split between them since "
        "the loop slowed, at VR90's polish time; an even split lands inside every band), gate oxide %s (the spring life replayed at the plan's bench loading, at VR90's gate oxide area), VR90's own "
        "edge die %s and the design-limited fallout the plan files, so %s per cent; as filed %s per cent; %s starts for the "
        "commitment at the plan's back-end yields."
        % (fg["vr90_random_yield_pct"], fg["vr90_fixed_parts"]["scratch"], fg["vr90_fixed_parts"]["gate_oxide"],
           fg["vr90_fixed_parts"]["edge_die"], fg["R6_fixed"], p["plan"], n(p["starts"])),
    ]
    for k, x in enumerate(st):
        L.append("%d. %s" % (k + 1, x))
    L.append("\nNo other conclusion survives the files. The far polishers' scratching cannot be their own consumables, because "
             "it fell to the spring level on every tap while the standby pump ran; CM3's tune cannot be the whole edge cause, "
             "because DP2B's wafers on CM3 are clean and its other wafers fail; the bench's state at the summer's loading "
             "cannot stand for Q1, because the drag is per lot and the plan runs more lots a day; a wafer counter cannot set the "
             "deep-etch cleans, because the monitors flake earlier wherever CT-DEEP-07 ran; the gate oxide loss cannot scale "
             "with the die, because oxide integrity fails with the gate oxide's own area, which the product data sheet "
             "carries for each product; a die-area formula cannot carry the yield to VR90's die, because the block "
             "yields fall far more slowly than a Poisson line; and four VX40 die tiled from January to March cannot stand "
             "for VR90 with every cause fixed (%s per cent), because they keep VX40's shorter polish, 2026's bench loading "
             "rather than the plan's, VX40's own share of CM3 and VX40's edge die." % fg["vr90_tile_fixed"])
    return "\n".join(L) + "\n"
