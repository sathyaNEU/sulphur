"""task16 submission.md: the four answer blocks, drafted from figures.json so every figure they state is one the
generator computed."""
import deliver as DL
import pack as PK


def n0(x):
    return "{:,.0f}".format(x)


def poisson_net(m, p_diff):
    """The 95 per cent interval on a rule's two-patient pairs from its clear discordant count (exact Poisson), net of
    the mislabelled specimens expected and scaled as the point estimate is."""
    from scipy.stats import chi2
    k, e = m["discordant_clear"], m["expected_one_patient_clear"]
    scale = m["links"] / max(m["typed_links_clear"], 1) / p_diff
    lo = chi2.ppf(0.025, 2 * k) / 2.0 if k > 0 else 0.0
    hi = chi2.ppf(0.975, 2 * k + 2) / 2.0
    return max(lo - e, 0.0) * scale, max(hi - e, 0.0) * scale


def rate_band(b, links):
    return [round(2000.0 * b[0] / links, 2), round(2000.0 * b[1] / links, 2)]


def derived(T, fo):
    """The figures the blocks state that are worked from others: each estimate's band per 2,000 links, the blood
    groups' interval on rule A, rule A's shares, the golden family's spread by rule and each rule's line."""
    L, B = T["rule_links"], T["bands"]
    est = {"A": B["R2_rule_a_false"], "B": B["R8_rule_b_false"], "C": B["R3_rule_c_false"], "D": B["R4_rule_d_false"]}
    lo, hi = poisson_net(T["marker"]["A"], T["marker_noise"]["p_diff"])
    fam = fo["family"]
    rng = {m: [min([T["rule_false"][m]] + [x["value"] for x in fam if x["member"] == m]),
               max([T["rule_false"][m]] + [x["value"] for x in fam if x["member"] == m])] for m in L}
    return {"rate_bands": {k: rate_band(est[k], L[k]) for k in L},
            "marker_a_interval": [int(round(lo)), int(round(hi))], "interval_level": 95,
            "rule_a_shares_pct": {k: int(round(100 * v)) for k, v in T["rule_a_shares"].items()},
            "family_range": {m: [round(v[0], 1), round(v[1], 1)] for m, v in rng.items()},
            "cap_lines": {k: round(L[k] / 2000.0, 1) for k in L}}


def rb(T, k):
    return "%.2f to %.2f" % tuple(T["rate_bands"][k])


def write(figs, G, fo, path):
    T = figs
    L, F_, Rt = T["rule_links"], T["rule_false"], T["rule_rate_per_2000"]
    I = T["incumbent_rate_per_2000"]
    mk, nz = T["marker"], T["marker_noise"]
    B = T["bands"]
    FN = PK.FILES
    rule = T["R6_rule"]
    doc, res, ovl, cap = T["documented"], T["resolve_b"], T["R9_overlay_links"], T["cap_lines"]
    CR = T["careful_rule_false"]
    routes = T["routes"]
    lines = []
    a = lines.append
    a("## Tags")
    a("")
    a("**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution: a merged "
      "health system's enterprise master patient index).")
    a("**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).")
    a("")
    a("## Final Recommendation")
    a("")
    a("**Run Rule %s at the One Chart conversion:** it joins %s pairs of records and about %s of them are two different "
      "patients (%.2f per 2,000 automatic links, inside HIM-14's one) once its %d blood-group mismatches are explained "
      "(%d on Calder Bay records that already hold two patients, split before the conversion; %d left as false merges). "
      "Reject Rule A (about %.0f false merges, %.2f per 2,000: names cluster by community and birth year and the men who "
      "came to work the boats carry 1 January document dates, which the engine's national rates (%.2f) and the blood "
      "bank's mostly older patients do not see), Rule C (about %s pairs of twins, %.2f per 2,000, of which the delivery "
      "log and the registration visits show only %d) and Rule D (%s, %.2f)." % (
          rule, n0(L[rule]), n0(F_[rule]), Rt[rule], res["discordant"], res["overlay"], res["left"],
          F_["A"], Rt["A"], I["A"], n0(F_["C"]), Rt["C"], doc["C"]["documented_twins"], n0(F_["D"]), Rt["D"]))
    a("")
    a("## Supplementary Questions")
    a("")
    a("### %s" % DL.WORKBOOK)
    a("")
    order = sorted(L, key=lambda k: -L[k])
    est = {"A": ("%.1f" % F_["A"], B["R2_rule_a_false"]), "B": (n0(F_["B"]), B["R8_rule_b_false"]),
           "C": (n0(F_["C"]), B["R3_rule_c_false"]), "D": (n0(F_["D"]), B["R4_rule_d_false"])}
    a("1. Rules sheet, one row per candidate rule ordered by automatic links, with columns rule, definition, automatic "
      "links, estimated false merges, false merges per 2,000 links and within the policy: %s; each rule's links are exact "
      "under the specification's standardization and within 0.1 per cent of these under another careful reading of "
      "it." % "; ".join(
          "Rule %s %s links, %s false merges (%s to %s), %.2f per 2,000 (%s), %s" % (
              k, n0(L[k]), est[k][0], n0(est[k][1][0]), n0(est[k][1][1]), Rt[k], rb(T, k),
              "inside the policy" if Rt[k] <= 1.0 else "over it") for k in order))
    a("2. Index sheet and Overlays to split sheet: %s Calder Bay records hold two or more patients (%s to %s), each "
      "listed with its surviving MRN, name and birth date." % (n0(T["R5_overlays"]), n0(B["R5_overlays"][0]),
                                                               n0(B["R5_overlays"][1])))
    r1, b1 = T["R1_index"], B["R1_index"]
    a("3. Index sheet: %s distinct patients in the converted index (%s to %s) and %s patients held by both Calder Bay "
      "and Rosario (%s to %s)." % (n0(r1["distinct patients"]), n0(b1["distinct patients"][0]),
                                   n0(b1["distinct patients"][1]), n0(r1["patients in both indexes"]),
                                   n0(b1["patients in both indexes"][0]), n0(b1["patients in both indexes"][1])))
    a("4. Index sheet: %s patients still under more than one active record once Rule %s's links are made (%s to %s)."
      % (n0(T["R7_left_after_rule"]), rule, n0(B["R7_left_after_rule"][0]), n0(B["R7_left_after_rule"][1])))
    b9 = B["R9_overlay_links"]
    a("5. Index sheet: %s of Rule %s's links touch a record that holds two or more patients (%s to %s), %s such records "
      "in all (%s to %s), each split before those links are made." % (
          n0(ovl["links"]), rule, n0(b9["links"][0]), n0(b9["links"][1]), n0(ovl["records split"]),
          n0(b9["records split"][0]), n0(b9["records split"][1])))
    a("")
    a("### %s" % DL.MEMO)
    a("")
    a("6. One page: run Rule %s, with its links and false merges per 2,000 and how its blood mismatches are explained; "
      "why not Rules A, C and D, each with its false merges per 2,000; the Calder Bay records that hold two or more "
      "patients and the links that touch them; the distinct patients, the patients both indexes hold and the patients "
      "left under more than one record." % rule)
    a("")
    a("## Critical Components")
    a("")
    ba, bc, bb = B["R2_rule_a_false"], B["R3_rule_c_false"], B["R8_rule_b_false"]
    a("1. Rule A's false merges: **%.1f** (%s to %s) of its %s links, **%.2f per 2,000** (%s, against one), from pairs "
      "of different patients who share first name, last name, sex and birth date; %d per cent of them among men born "
      "since 1975 and %d per cent among patients born before 1960." % (
          F_["A"], n0(ba[0]), n0(ba[1]), n0(L["A"]), Rt["A"], rb(T, "A"), T["rule_a_shares_pct"]["men_since_1975"],
          T["rule_a_shares_pct"]["before_1960"]))
    a("2. Rule C's false merges: **%s** pairs of twins (%s to %s) among its %s links, **%.2f per 2,000** (%s), of which "
      "the delivery log and one registration visit show only **%d**." % (
          n0(F_["C"]), n0(bc[0]), n0(bc[1]), n0(L["C"]), Rt["C"], rb(T, "C"), doc["C"]["documented_twins"]))
    a("3. Rule B's false merges once its blood mismatches are explained: **%s** (%s to %s), **%.2f per 2,000**: of its "
      "**%d** links whose records differ in ABO group or Rh type, **%d** touch a Calder Bay record that holds two "
      "patients (%d of them under one SSN), **%d** a record whose own typings disagree, and **%d** %s left as false "
      "merges, beside the twins one registration visit shows." % (
          n0(F_["B"]), n0(bb[0]), n0(bb[1]), Rt["B"], res["discordant"], res["overlay"], res["overlay_same_ssn"],
          res["mislabel"], res["left"], "is" if res["left"] == 1 else "are"))
    a("")
    a("## Step-by-Step")
    a("")
    a("1. Read %s and %s into one table of %s active records, compared as %s standardizes them (names upper-cased "
      "with hyphens as spaces, unit designators off the street address, ten-digit phones, all-zero and all-nine SSNs "
      "missing)." % (FN["index_a"], FN["index_b"], n0(T["active_records"]), FN["spec"]))
    a("2. Applied each rule of %s section 7.2 to every pair of active records across and within the two indexes: Rule "
      "A %s links, Rule C %s, Rule D %s, Rule B %s; their lines under HIM-14 are %.1f, %.1f, %.1f and %.1f false merges."
      % (FN["plan"], n0(L["A"]), n0(L["C"]), n0(L["D"]), n0(L["B"]), cap["A"], cap["C"], cap["D"], cap["B"]))
    a("3. Rule A: the specification's national rates put chance agreement on all four fields at %.1f merges here and the "
      "records' own field rates at %.1f, both inside its line; counting the pairs of patients who share first name, last "
      "name, sex and birth year, each pair's chance of one birth date taken from its surname community's 1 January and "
      "1 July shares by decade (shrunk toward the decade's), gives %.1f, %.2f per 2,000, %d per cent of it among men born "
      "since 1975, who came to work the boats and the yards with document dates." % (
          T["indep_vendor"], T["indep_local"], F_["A"], Rt["A"], T["rule_a_shares_pct"]["men_since_1975"]))
    ma = mk["A"]
    lo, hi = T["marker_a_interval"]
    a("4. The blood bank cannot settle Rule A: of its links whose records both carry results (%s), %d differ in ABO "
      "group or Rh type, %d on a record that holds two patients and about %.1f what mislabelled specimens give; among "
      "the links Rule B "
      "does not make, %d discordant pair%s carry different SSNs, which looks like the national rate; but typed patients "
      "were born %d years earlier on average than Rule A's linked patients, so the groups see almost none of the men and "
      "children where its chance merges sit (net of both errors, %.0f, %d per cent interval %d to %d)." % (
          n0(ma["typed_links"]), ma["discordant"], ma["discordant"] - ma["discordant_clear"], ma["expected_one_patient_clear"],
          doc["A"]["discordant_other_ssn"], "" if doc["A"]["discordant_other_ssn"] == 1 else "s",
          T["marker_a_birth_year"]["years_older"], ma["net"], T["interval_level"], lo, hi))
    a("5. Rule C: %s reviewed none of Rule C's links, and the delivery log's two newborns of one delivery and the records "
      "made on one registration visit document only %d twin pairs among them, under its line of %.1f; but most twins here "
      "were registered on separate visits or born before their families came to Port Calder. Linking the index on every "
      "field the rules do not compare (each twin's own SSN, phone and visit history, with the documented pairs kept "
      "apart) keeps %s pairs of twins apart that Rule C joins, %.2f per 2,000, at a match probability of 0.3 or 0.7 alike."
      % (FN["pilot"], doc["C"]["documented_twins"], cap["C"], n0(F_["C"]), Rt["C"]))
    a("6. Rule D: a family's SSN on several children's records joins %s pairs of two patients, %.2f per 2,000; the "
      "delivery log and one visit alone already show %d." % (n0(F_["D"]), Rt["D"], doc["D"]["documented_twins"]))
    a("7. Overlays: %s shows Calder Bay's automatic merges from March 2019 joined new registrations on last name, birth "
      "date and sex alone; reading each retired record's first name against its survivor's (forms of one name in %s "
      "and typing slips as one patient), %s surviving records hold two or more patients, where every merge whose names "
      "differ as typed would give %s." % (FN["merges"], FN["names"], n0(T["R5_overlays"]), n0(T["overlays_as_typed"])))
    a("8. Rule B: %d of its typed links differ in ABO group or Rh type, which read as false merges and scaled from "
      "the typed links would put it at %.0f, over its line of %.1f; %d of them touch one of those overlaid records (the "
      "record also holds "
      "a second patient's typing; HIM-14 section 4 splits it before the conversion), %d %s a record whose own typings "
      "disagree, and %d %s left as false merges, which with the twins one visit shows gives %s, %.2f per 2,000. %s of "
      "its links touch %s overlaid records." % (
          res["discordant"], mk["B"]["as_read"], cap["B"], res["overlay"], res["mislabel"],
          "is" if res["mislabel"] == 1 else "are", res["left"], "is" if res["left"] == 1 else "are", n0(F_["B"]), Rt["B"],
          n0(ovl["links"]), n0(ovl["records split"])))
    a("9. The linked index: Fellegi-Sunter weights fitted by EM on the candidate pairs, the evidence above keeping two "
      "patients apart and the merge history's retired records included, gives %s distinct patients, %s held by both "
      "indexes, and %s still under more than one active record once Rule %s's links are made." % (
          n0(r1["distinct patients"]), n0(r1["patients in both indexes"]), n0(T["R7_left_after_rule"]), rule))
    a("10. Under %s section 3 only Rule %s is inside one false merge per 2,000 automatic links (%.2f), so the conversion "
      "runs it." % (FN["policy"], rule, Rt[rule]))
    a("")
    fr = T["family_range"]
    a("No other rule survives. Rule A stays over its line however its communities' 1 January shares are estimated (%.1f "
      "to %.1f against %.1f), Rule C on the linkage at either threshold (%s), Rule D on names alone or with blood groups "
      "(%s to %s), and Rule B under its line on every reading of its mismatches (%s against %.1f). Each shortcut "
      "lands on another answer: the documented failures counted with Rule B's mismatches held, as a careful but hurried "
      "pass reads the files, runs Rule A; correcting Rule A alone runs Rule C; holding Rule B's mismatches with A and C "
      "right runs no rule; the blood groups read as they stand condemn every rule." % (
          fr["A"][0], fr["A"][1], cap["A"], n0(fr["C"][0]), n0(fr["D"][0]), n0(fr["D"][1]),
          ("%s on each" % n0(fr["B"][0])) if n0(fr["B"][0]) == n0(fr["B"][1]) else
          ("%s to %s" % (n0(fr["B"][0]), n0(fr["B"][1]))), cap["B"]))
    open(path, "w").write("\n".join(lines) + "\n")
